"""
Review Analysis — Sentiment Analysis & Aspect-Based Sentiment

Multi-layer sentiment analysis for hotel reviews:
1. Overall sentiment classification (positive/mixed/negative)
2. Aspect-based sentiment (cleanliness, staff, food, location, value)
3. Trend analysis over time
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "review_analysis"

ASPECTS = ["cleanliness", "staff", "food", "location", "value"]

# Aspect keyword dictionaries for rule-based extraction
ASPECT_KEYWORDS = {
    "cleanliness": [
        "clean", "dirty", "spotless", "stain", "dust", "hygiene", "tidy",
        "housekeeping", "maintained", "pristine", "filthy", "mold",
    ],
    "staff": [
        "staff", "reception", "service", "friendly", "helpful", "rude",
        "concierge", "welcoming", "attentive", "responsive", "professional",
    ],
    "food": [
        "breakfast", "dinner", "restaurant", "food", "buffet", "meal",
        "chef", "delicious", "bland", "menu", "cuisine", "room service",
    ],
    "location": [
        "location", "central", "distance", "transport", "walk", "nearby",
        "neighborhood", "surroundings", "view", "beach", "city center",
    ],
    "value": [
        "price", "value", "expensive", "cheap", "overpriced", "worth",
        "affordable", "cost", "money", "deal", "budget",
    ],
}

# Sentiment words
POSITIVE_WORDS = {
    "excellent", "amazing", "wonderful", "fantastic", "outstanding", "perfect",
    "great", "superb", "exceptional", "brilliant", "lovely", "delightful",
    "impressive", "best", "recommend", "loved", "enjoyed", "beautiful",
}
NEGATIVE_WORDS = {
    "terrible", "awful", "horrible", "worst", "disgusting", "disappointing",
    "poor", "bad", "dirty", "rude", "overpriced", "noisy", "broken",
    "uncomfortable", "unacceptable", "never", "complaint", "avoid",
}


class SentimentAnalyzer:
    """Multi-method sentiment analysis for hotel reviews."""

    def __init__(self):
        self.ml_model = None
        self.aspect_models = {}

    def rule_based_sentiment(self, text: str) -> dict:
        """Rule-based sentiment using keyword matching."""
        text_lower = text.lower()
        words = set(re.findall(r'\w+', text_lower))

        pos_count = len(words & POSITIVE_WORDS)
        neg_count = len(words & NEGATIVE_WORDS)

        if pos_count > neg_count * 1.5:
            sentiment = "positive"
        elif neg_count > pos_count * 1.5:
            sentiment = "negative"
        else:
            sentiment = "mixed"

        confidence = abs(pos_count - neg_count) / max(pos_count + neg_count, 1)
        return {"sentiment": sentiment, "confidence": round(confidence, 3)}

    def extract_aspects(self, text: str) -> dict:
        """Extract which aspects are mentioned in the review."""
        text_lower = text.lower()
        mentioned = {}

        for aspect, keywords in ASPECT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    mentioned[aspect] = True
                    break
            else:
                mentioned[aspect] = False

        return mentioned

    def aspect_sentiment(self, text: str) -> dict:
        """Determine sentiment for each mentioned aspect."""
        text_lower = text.lower()
        results = {}

        for aspect, keywords in ASPECT_KEYWORDS.items():
            # Find sentences mentioning this aspect
            sentences = text_lower.split(".")
            aspect_sentences = [
                s for s in sentences
                if any(kw in s for kw in keywords)
            ]

            if not aspect_sentences:
                results[aspect] = {"mentioned": False, "sentiment": None}
                continue

            # Analyze sentiment of aspect-related sentences
            combined = " ".join(aspect_sentences)
            words = set(re.findall(r'\w+', combined))
            pos = len(words & POSITIVE_WORDS)
            neg = len(words & NEGATIVE_WORDS)

            if pos > neg:
                sent = "positive"
            elif neg > pos:
                sent = "negative"
            else:
                sent = "neutral"

            results[aspect] = {"mentioned": True, "sentiment": sent}

        return results

    def train_ml_model(self, df: pd.DataFrame) -> dict:
        """Train ML-based sentiment classifier."""
        X_train, X_test, y_train, y_test = train_test_split(
            df["review_text"], df["sentiment_true"],
            test_size=0.2, random_state=42, stratify=df["sentiment_true"],
        )

        # TF-IDF + Gradient Boosting
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=8000, ngram_range=(1, 2),
                sublinear_tf=True, min_df=2,
            )),
            ("clf", GradientBoostingClassifier(
                n_estimators=200, max_depth=5,
                learning_rate=0.1, random_state=42,
            )),
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(pipeline, df["review_text"], df["sentiment_true"], cv=5, scoring="accuracy")

        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

        self.ml_model = pipeline

        logger.info(f"\nML Sentiment Model:")
        logger.info(f"  Accuracy: {accuracy:.4f}")
        logger.info(f"  CV Accuracy: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
        logger.info(f"\n{classification_report(y_test, y_pred, zero_division=0)}")

        return {
            "accuracy": round(accuracy, 4),
            "cv_accuracy": round(cv_scores.mean(), 4),
            "cv_std": round(cv_scores.std(), 4),
            "report": report,
        }

    def train_aspect_models(self, df: pd.DataFrame) -> dict:
        """Train ML models for each aspect score prediction."""
        results = {}

        for aspect in ASPECTS:
            col = f"aspect_{aspect}"
            if col not in df.columns:
                continue

            # Binary: good (4-5) vs bad (1-3)
            y = (df[col] >= 4).astype(int)

            pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=1000, random_state=42)),
            ])

            cv_scores = cross_val_score(pipeline, df["review_text"], y, cv=5, scoring="accuracy")
            pipeline.fit(df["review_text"], y)
            self.aspect_models[aspect] = pipeline

            results[aspect] = {
                "cv_accuracy": round(cv_scores.mean(), 4),
                "cv_std": round(cv_scores.std(), 4),
            }
            logger.info(f"  {aspect:15s} CV Accuracy: {cv_scores.mean():.4f}")

        return results

    def analyze_trends(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze sentiment trends over time."""
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df["year_month"] = df["date"].dt.to_period("M").astype(str)

        trends = df.groupby("year_month").agg(
            avg_rating=("rating", "mean"),
            review_count=("review_id", "count"),
            positive_pct=("sentiment_true", lambda x: (x == "positive").mean() * 100),
            negative_pct=("sentiment_true", lambda x: (x == "negative").mean() * 100),
        ).round(2)

        # Aspect trends
        for aspect in ASPECTS:
            col = f"aspect_{aspect}"
            if col in df.columns:
                trends[f"avg_{aspect}"] = df.groupby("year_month")[col].mean().round(2)

        return trends


def run_review_analysis(df: pd.DataFrame) -> dict:
    """Run complete review analysis pipeline."""
    logger.info("=" * 60)
    logger.info("  REVIEW ANALYSIS PIPELINE")
    logger.info("=" * 60)

    analyzer = SentimentAnalyzer()

    # 1. Rule-based sentiment
    logger.info("\n--- Rule-Based Sentiment ---")
    df = df.copy()
    rule_results = df["review_text"].apply(analyzer.rule_based_sentiment)
    df["rule_sentiment"] = [r["sentiment"] for r in rule_results]
    rule_accuracy = (df["rule_sentiment"] == df["sentiment_true"]).mean()
    logger.info(f"  Rule-based accuracy: {rule_accuracy:.4f}")

    # 2. ML sentiment model
    logger.info("\n--- ML Sentiment Model ---")
    ml_results = analyzer.train_ml_model(df)

    # 3. Aspect models
    logger.info("\n--- Aspect Sentiment Models ---")
    aspect_results = analyzer.train_aspect_models(df)

    # 4. Aspect extraction (rule-based)
    logger.info("\n--- Aspect Extraction ---")
    aspect_mentions = df["review_text"].apply(analyzer.extract_aspects)
    for aspect in ASPECTS:
        mention_rate = sum(1 for r in aspect_mentions if r[aspect]) / len(df) * 100
        logger.info(f"  {aspect:15s} mentioned in {mention_rate:.1f}% of reviews")

    # 5. Trends
    logger.info("\n--- Sentiment Trends ---")
    trends = analyzer.analyze_trends(df)
    logger.info(f"  {len(trends)} months of trend data")

    # Save models and results
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if analyzer.ml_model:
        joblib.dump(analyzer.ml_model, MODELS_DIR / "sentiment_model.joblib")
    for aspect, model in analyzer.aspect_models.items():
        joblib.dump(model, MODELS_DIR / f"aspect_{aspect}_model.joblib")

    trends.to_csv(MODELS_DIR / "sentiment_trends.csv")

    summary = {
        "rule_based_accuracy": round(rule_accuracy, 4),
        "ml_accuracy": ml_results["accuracy"],
        "ml_cv_accuracy": ml_results["cv_accuracy"],
        "aspect_models": aspect_results,
        "total_reviews": len(df),
    }
    with open(MODELS_DIR / "analysis_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\nResults saved to {MODELS_DIR}")
    return summary


def main():
    df = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "reviews.csv")
    run_review_analysis(df)


if __name__ == "__main__":
    main()
