"""
Booking Cancellation — Model Training & Evaluation

Trains and compares multiple classification models:
1. Logistic Regression (baseline)
2. Random Forest
3. XGBoost
4. LightGBM
5. CatBoost

Includes cross-validation, hyperparameter tuning, and comprehensive
evaluation metrics (AUC-ROC, Precision, Recall, F1).
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, classification_report, confusion_matrix,
    precision_score, recall_score, f1_score, accuracy_score,
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "cancellation"
RANDOM_SEED = 42


def prepare_data(df: pd.DataFrame, feature_cols: list) -> dict:
    """Split data into train/test sets."""
    X = df[feature_cols].copy()
    y = df["is_canceled"].copy()

    # Handle any remaining NaN/inf
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
    logger.info(f"Train cancel rate: {y_train.mean():.3f}, Test: {y_test.mean():.3f}")

    return {
        "X_train": X_train, "X_test": X_test,
        "y_train": y_train, "y_test": y_test,
        "feature_names": feature_cols,
    }


def get_models() -> dict:
    """Define models with tuned hyperparameters."""
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_SEED,
            class_weight="balanced",
            C=0.1,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=RANDOM_SEED,
            n_jobs=-1,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            scale_pos_weight=1.5,
            random_state=RANDOM_SEED,
            eval_metric="auc",
            verbosity=0,
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=300,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            is_unbalance=True,
            random_state=RANDOM_SEED,
            verbose=-1,
        ),
        "CatBoost": CatBoostClassifier(
            iterations=300,
            depth=6,
            learning_rate=0.1,
            auto_class_weights="Balanced",
            random_seed=RANDOM_SEED,
            verbose=0,
        ),
    }
    return models


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """Evaluate a single model and return metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model_name": model_name,
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1": round(f1_score(y_test, y_pred), 4),
        "auc_roc": round(roc_auc_score(y_test, y_proba), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    logger.info(f"\n{'='*50}")
    logger.info(f"  {model_name}")
    logger.info(f"{'='*50}")
    logger.info(f"  AUC-ROC:   {metrics['auc_roc']}")
    logger.info(f"  Accuracy:  {metrics['accuracy']}")
    logger.info(f"  Precision: {metrics['precision']}")
    logger.info(f"  Recall:    {metrics['recall']}")
    logger.info(f"  F1-Score:  {metrics['f1']}")

    return metrics


def cross_validate_model(model, X_train, y_train, model_name: str) -> dict:
    """Run stratified k-fold cross-validation."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

    scoring = ["roc_auc", "f1", "precision", "recall"]
    cv_results = cross_validate(
        model, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1
    )

    cv_metrics = {
        f"cv_{metric}": round(cv_results[f"test_{metric}"].mean(), 4)
        for metric in scoring
    }
    cv_metrics.update({
        f"cv_{metric}_std": round(cv_results[f"test_{metric}"].std(), 4)
        for metric in scoring
    })

    logger.info(f"  CV AUC-ROC: {cv_metrics['cv_roc_auc']:.4f} +/- {cv_metrics['cv_roc_auc_std']:.4f}")
    return cv_metrics


def train_all_models(data: dict) -> tuple[dict, dict]:
    """Train all models and return results."""
    models = get_models()
    all_results = {}
    trained_models = {}

    X_train, X_test = data["X_train"], data["X_test"]
    y_train, y_test = data["y_train"], data["y_test"]

    # Scale features for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test), columns=X_test.columns, index=X_test.index
    )

    for name, model in models.items():
        logger.info(f"\nTraining {name}...")

        # Use scaled data for Logistic Regression
        if name == "Logistic Regression":
            model.fit(X_train_scaled, y_train)
            test_metrics = evaluate_model(model, X_test_scaled, y_test, name)
            cv_metrics = cross_validate_model(model, X_train_scaled, y_train, name)
        else:
            model.fit(X_train, y_train)
            test_metrics = evaluate_model(model, X_test, y_test, name)
            cv_metrics = cross_validate_model(model, X_train, y_train, name)

        all_results[name] = {**test_metrics, **cv_metrics}
        trained_models[name] = model

    trained_models["scaler"] = scaler
    return all_results, trained_models


def select_best_model(results: dict) -> str:
    """Select best model based on AUC-ROC."""
    best_name = max(results, key=lambda k: results[k]["auc_roc"])
    logger.info(f"\nBest model: {best_name} (AUC-ROC: {results[best_name]['auc_roc']})")
    return best_name


def save_results(results: dict, trained_models: dict, best_model_name: str, data: dict):
    """Save trained models and results."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Save best model
    best_model = trained_models[best_model_name]
    joblib.dump(best_model, MODELS_DIR / "best_model.joblib")
    joblib.dump(trained_models["scaler"], MODELS_DIR / "scaler.joblib")

    # Save all models
    for name, model in trained_models.items():
        if name != "scaler":
            safe_name = name.lower().replace(" ", "_")
            joblib.dump(model, MODELS_DIR / f"{safe_name}.joblib")

    # Save results
    results_df = pd.DataFrame(results).T
    results_df.to_csv(MODELS_DIR / "model_comparison.csv")

    # Save metadata
    metadata = {
        "best_model": best_model_name,
        "best_auc_roc": results[best_model_name]["auc_roc"],
        "feature_count": len(data["feature_names"]),
        "train_size": len(data["X_train"]),
        "test_size": len(data["X_test"]),
        "feature_names": data["feature_names"],
    }
    with open(MODELS_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Models saved to {MODELS_DIR}")


def run_training_pipeline(df: pd.DataFrame, feature_cols: list) -> dict:
    """Run the complete training pipeline."""
    logger.info("=" * 60)
    logger.info("  MODEL TRAINING PIPELINE")
    logger.info("=" * 60)

    data = prepare_data(df, feature_cols)
    results, trained_models = train_all_models(data)
    best_model_name = select_best_model(results)
    save_results(results, trained_models, best_model_name, data)

    # Print comparison table
    logger.info("\n" + "=" * 60)
    logger.info("  MODEL COMPARISON SUMMARY")
    logger.info("=" * 60)
    comparison = pd.DataFrame({
        name: {
            "AUC-ROC": r["auc_roc"],
            "F1": r["f1"],
            "Precision": r["precision"],
            "Recall": r["recall"],
            "CV AUC-ROC": r["cv_roc_auc"],
        }
        for name, r in results.items()
    }).T
    logger.info(f"\n{comparison.to_string()}")

    return {
        "results": results,
        "trained_models": trained_models,
        "best_model_name": best_model_name,
        "data": data,
    }


def main():
    from src.module_1_predictive.cancellation.eda import load_data
    from src.module_1_predictive.cancellation.features import run_feature_engineering

    df = load_data()
    df, feature_cols = run_feature_engineering(df)
    run_training_pipeline(df, feature_cols)


if __name__ == "__main__":
    main()
