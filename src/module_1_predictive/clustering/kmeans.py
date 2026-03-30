"""
Customer Segmentation — K-Means Clustering + Classification

1. K-Means clustering with optimal k selection (Elbow + Silhouette)
2. Segment profiling and business interpretation
3. Supervised classifier to assign new customers to segments
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "segmentation"
RANDOM_SEED = 42


def select_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Select and scale numeric features for clustering."""
    exclude_cols = {"customer_id", "segment_true", "customer_type"}
    feature_cols = [
        col for col in df.columns
        if col not in exclude_cols
        and df[col].dtype in [np.int64, np.float64, np.int32, np.float32]
    ]

    X = df[feature_cols].copy()
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())

    return X, feature_cols


def find_optimal_k(X_scaled: np.ndarray, k_range: range = range(2, 11)) -> dict:
    """Find optimal number of clusters using Elbow and Silhouette methods."""
    results = {"k": [], "inertia": [], "silhouette": []}

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        results["k"].append(k)
        results["inertia"].append(kmeans.inertia_)
        results["silhouette"].append(silhouette_score(X_scaled, labels))

        logger.info(f"  k={k}: Inertia={kmeans.inertia_:.0f}, Silhouette={results['silhouette'][-1]:.4f}")

    # Best k by silhouette
    best_idx = np.argmax(results["silhouette"])
    best_k = results["k"][best_idx]
    logger.info(f"\nOptimal k by Silhouette: {best_k} (score: {results['silhouette'][best_idx]:.4f})")

    return {"results": results, "optimal_k": best_k}


def fit_kmeans(X_scaled: np.ndarray, k: int) -> tuple:
    """Fit final K-Means model."""
    kmeans = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init=20)
    labels = kmeans.fit_predict(X_scaled)

    sil_score = silhouette_score(X_scaled, labels)
    logger.info(f"Final K-Means: k={k}, Silhouette={sil_score:.4f}")

    return kmeans, labels


def profile_segments(df: pd.DataFrame, labels: np.ndarray, feature_cols: list) -> pd.DataFrame:
    """Create business profiles for each segment."""
    df = df.copy()
    df["cluster"] = labels

    # Key metrics per segment
    profile_cols = [
        "recency", "frequency", "total_revenue", "avg_revenue",
        "avg_nights", "avg_daily_rate", "avg_extra_spend",
        "booking_frequency", "revenue_consistency", "resort_ratio",
    ]
    available_cols = [c for c in profile_cols if c in df.columns]

    profiles = df.groupby("cluster")[available_cols].agg(["mean", "median", "count"]).round(2)

    # Assign business names based on cluster characteristics
    cluster_summary = df.groupby("cluster").agg(
        avg_revenue=("total_revenue", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_recency=("recency", "mean"),
        count=("customer_id", "count"),
    ).round(2)

    # Sort by revenue to assign names
    sorted_clusters = cluster_summary.sort_values("avg_revenue", ascending=False)

    segment_names = {}
    name_pool = [
        "Premium Guests", "Loyal Regulars", "Growing Potential",
        "Occasional Visitors", "Budget Travelers", "Inactive/Lost",
        "Business Elite", "Seasonal Visitors",
    ]

    for i, (cluster_id, _) in enumerate(sorted_clusters.iterrows()):
        if i < len(name_pool):
            segment_names[cluster_id] = name_pool[i]
        else:
            segment_names[cluster_id] = f"Segment {cluster_id}"

    df["segment_name"] = df["cluster"].map(segment_names)

    logger.info("\nSegment Profiles:")
    for cluster_id, name in segment_names.items():
        subset = df[df["cluster"] == cluster_id]
        logger.info(f"\n  {name} (n={len(subset)})")
        logger.info(f"    Avg Revenue: EUR {subset['total_revenue'].mean():,.2f}")
        logger.info(f"    Avg Frequency: {subset['frequency'].mean():.1f}")
        logger.info(f"    Avg Recency: {subset['recency'].mean():.0f} days")

    return df


def train_segment_classifier(df: pd.DataFrame, feature_cols: list) -> dict:
    """Train a supervised classifier to assign new customers to segments."""
    X = df[feature_cols].copy()
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    y = df["cluster"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Cross-validation
    cv_scores = cross_val_score(clf, X, y, cv=5, scoring="accuracy")

    logger.info(f"\nSegment Classifier:")
    logger.info(f"  Test Accuracy: {report['accuracy']:.4f}")
    logger.info(f"  CV Accuracy: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

    # Feature importance
    importance = pd.Series(clf.feature_importances_, index=feature_cols).sort_values(ascending=False)
    logger.info(f"\nTop 10 features for segment prediction:")
    for feat, imp in importance.head(10).items():
        logger.info(f"  {feat:35s} {imp:.4f}")

    return {
        "classifier": clf,
        "report": report,
        "cv_accuracy": round(cv_scores.mean(), 4),
        "feature_importance": importance,
    }


def run_segmentation_pipeline() -> dict:
    """Run the complete customer segmentation pipeline."""
    logger.info("=" * 60)
    logger.info("  CUSTOMER SEGMENTATION PIPELINE")
    logger.info("=" * 60)

    # Load features
    from src.module_1_predictive.clustering.features import create_clustering_features
    df = create_clustering_features()

    # Select and scale
    X, feature_cols = select_features(df)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Find optimal k
    logger.info("\n--- Optimal K Selection ---")
    k_analysis = find_optimal_k(X_scaled)
    optimal_k = k_analysis["optimal_k"]

    # Fit K-Means
    logger.info(f"\n--- Fitting K-Means (k={optimal_k}) ---")
    kmeans_model, labels = fit_kmeans(X_scaled, optimal_k)

    # Profile segments
    logger.info("\n--- Segment Profiling ---")
    df = profile_segments(df, labels, feature_cols)

    # Train classifier
    logger.info("\n--- Segment Classifier ---")
    clf_results = train_segment_classifier(df, feature_cols)

    # Save everything
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR = ROOT_DIR / "data" / "processed"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(kmeans_model, MODELS_DIR / "kmeans_model.joblib")
    joblib.dump(scaler, MODELS_DIR / "scaler.joblib")
    joblib.dump(clf_results["classifier"], MODELS_DIR / "segment_classifier.joblib")

    df.to_csv(OUTPUT_DIR / "customers_segments.csv", index=False)

    # Save summary
    summary = {
        "optimal_k": optimal_k,
        "silhouette_score": round(silhouette_score(X_scaled, labels), 4),
        "segment_counts": df["segment_name"].value_counts().to_dict(),
        "classifier_accuracy": clf_results["cv_accuracy"],
        "k_analysis": {
            "k_values": k_analysis["results"]["k"],
            "silhouette_scores": [round(s, 4) for s in k_analysis["results"]["silhouette"]],
        },
    }
    with open(MODELS_DIR / "segmentation_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\nAll results saved to {MODELS_DIR}")

    return {
        "df": df,
        "kmeans": kmeans_model,
        "classifier": clf_results,
        "summary": summary,
    }


def main():
    run_segmentation_pipeline()


if __name__ == "__main__":
    main()
