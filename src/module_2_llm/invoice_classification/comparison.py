"""
Invoice Classification — Method Comparison

Compares all classification approaches:
1. Rule-based (regex + keywords)
2. LLM Zero-shot
3. LLM Few-shot
4. Transformer (fine-tuned text classification)

Evaluates accuracy, speed, and cost trade-offs.
"""

import pandas as pd
import numpy as np
import time
import json
from pathlib import Path
import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "invoice_classification"


def train_tfidf_classifier(df: pd.DataFrame) -> dict:
    """Train a TF-IDF + classifier model as ML baseline."""
    X_train, X_test, y_train, y_test = train_test_split(
        df["description"], df["category_true"],
        test_size=0.2, random_state=42, stratify=df["category_true"],
    )

    # TF-IDF + Logistic Regression
    pipeline_lr = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, random_state=42, C=1.0)),
    ])

    # TF-IDF + Random Forest
    pipeline_rf = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)),
    ])

    results = {}

    for name, pipeline in [("TF-IDF + LogReg", pipeline_lr), ("TF-IDF + RF", pipeline_rf)]:
        start = time.time()
        pipeline.fit(X_train, y_train)
        train_time = time.time() - start

        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        cv_scores = cross_val_score(pipeline, df["description"], df["category_true"], cv=5, scoring="accuracy")

        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        results[name] = {
            "method": name,
            "accuracy": round(accuracy, 4),
            "cv_accuracy": round(cv_scores.mean(), 4),
            "cv_std": round(cv_scores.std(), 4),
            "train_time_seconds": round(train_time, 2),
            "report": report,
        }

        logger.info(f"\n{name}:")
        logger.info(f"  Accuracy: {accuracy:.4f}")
        logger.info(f"  CV Accuracy: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
        logger.info(f"  Train time: {train_time:.2f}s")

    # Save best ML model
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    best_name = max(results, key=lambda k: results[k]["accuracy"])
    best_pipeline = pipeline_lr if "LogReg" in best_name else pipeline_rf
    joblib.dump(best_pipeline, MODELS_DIR / "tfidf_classifier.joblib")

    return results


def run_comparison(df: pd.DataFrame) -> dict:
    """Run all methods and produce comparison report."""
    logger.info("=" * 60)
    logger.info("  INVOICE CLASSIFICATION — METHOD COMPARISON")
    logger.info("=" * 60)

    all_results = {}

    # 1. Rule-based
    logger.info("\n--- Rule-Based ---")
    from src.module_2_llm.invoice_classification.rule_based import (
        run_rule_based_classification, evaluate,
    )
    start = time.time()
    df_ruled = run_rule_based_classification(df)
    rule_time = time.time() - start
    rule_results = evaluate(df_ruled)
    rule_results["inference_time_seconds"] = round(rule_time, 2)
    all_results["Rule-Based"] = rule_results

    # 2. TF-IDF classifiers
    logger.info("\n--- TF-IDF Classifiers ---")
    tfidf_results = train_tfidf_classifier(df)
    all_results.update(tfidf_results)

    # 3. LLM (on sample — full dataset would be too expensive/slow)
    logger.info("\n--- LLM Classification (sample) ---")
    from src.module_2_llm.invoice_classification.llm_classifier import evaluate_llm
    sample = df.sample(min(300, len(df)), random_state=42)

    start = time.time()
    llm_few = evaluate_llm(sample, mode="few_shot")
    llm_time = time.time() - start
    llm_few["inference_time_seconds"] = round(llm_time, 2)
    llm_few["sample_size"] = len(sample)
    all_results["LLM Few-Shot"] = llm_few

    # Summary table
    logger.info("\n" + "=" * 60)
    logger.info("  COMPARISON SUMMARY")
    logger.info("=" * 60)

    summary = pd.DataFrame({
        name: {
            "Accuracy": r["accuracy"],
            "Method": r.get("method", name),
        }
        for name, r in all_results.items()
    }).T
    logger.info(f"\n{summary.to_string()}")

    # Save comparison
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    comparison_data = {
        name: {k: v for k, v in r.items() if k != "report"}
        for name, r in all_results.items()
    }
    with open(MODELS_DIR / "comparison_results.json", "w") as f:
        json.dump(comparison_data, f, indent=2, default=str)

    logger.info(f"\nResults saved to {MODELS_DIR}")
    return all_results


def main():
    df = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "invoices.csv")
    run_comparison(df)


if __name__ == "__main__":
    main()
