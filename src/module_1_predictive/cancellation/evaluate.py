"""
Booking Cancellation — SHAP Analysis & Business Impact

- SHAP feature importance and explanations
- Business impact calculation (revenue saved from correct predictions)
- Threshold optimization for business objectives
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json

from sklearn.metrics import precision_recall_curve, roc_curve
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "cancellation"


def compute_shap_values(model, X_test: pd.DataFrame, model_name: str) -> dict:
    """Compute SHAP values for model explainability."""
    try:
        import shap

        # Use appropriate explainer based on model type
        if "XGB" in type(model).__name__ or "LGBM" in type(model).__name__:
            explainer = shap.TreeExplainer(model)
        elif "CatBoost" in type(model).__name__:
            explainer = shap.TreeExplainer(model)
        elif "RandomForest" in type(model).__name__:
            explainer = shap.TreeExplainer(model)
        else:
            # For logistic regression use a sample
            sample = X_test.sample(min(500, len(X_test)), random_state=42)
            explainer = shap.LinearExplainer(model, sample)

        # Compute on a sample for speed
        X_sample = X_test.sample(min(2000, len(X_test)), random_state=42)
        shap_values = explainer.shap_values(X_sample)

        # Handle multi-output (binary classification)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        # Feature importance from SHAP
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        feature_importance = pd.Series(
            mean_abs_shap, index=X_sample.columns
        ).sort_values(ascending=False)

        logger.info(f"\nTop 15 features by SHAP importance ({model_name}):")
        for feat, imp in feature_importance.head(15).items():
            logger.info(f"  {feat:40s} {imp:.4f}")

        return {
            "shap_values": shap_values,
            "feature_importance": feature_importance,
            "X_sample": X_sample,
        }
    except Exception as e:
        logger.warning(f"SHAP computation failed: {e}")
        return None


def calculate_business_impact(
    y_test: pd.Series,
    y_proba: np.ndarray,
    adr_values: pd.Series,
    nights_values: pd.Series,
) -> dict:
    """Calculate business impact of the cancellation prediction model."""

    # Average values for estimation
    avg_adr = adr_values.mean()
    avg_nights = nights_values.mean()
    avg_booking_value = avg_adr * avg_nights

    # Overbooking parameters
    overbooking_recovery_rate = 0.70  # % of revenue recovered through overbooking
    deposit_recovery_rate = 0.50  # % recovered through deposit enforcement
    campaign_conversion_rate = 0.15  # % of at-risk bookings saved through campaigns

    results = {}

    # Analyze at different thresholds
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]

    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)

        tp = ((y_pred == 1) & (y_test == 1)).sum()  # Correctly predicted cancellations
        fp = ((y_pred == 1) & (y_test == 0)).sum()  # False alarms
        fn = ((y_pred == 0) & (y_test == 1)).sum()  # Missed cancellations
        tn = ((y_pred == 0) & (y_test == 0)).sum()  # Correctly predicted non-cancellations

        # Revenue impact calculation
        # 1. Revenue saved through overbooking (true positives)
        revenue_overbooking = tp * avg_booking_value * overbooking_recovery_rate

        # 2. Revenue saved through deposit enforcement
        revenue_deposit = tp * avg_booking_value * deposit_recovery_rate * 0.3

        # 3. Revenue saved through retention campaigns
        revenue_campaigns = tp * avg_booking_value * campaign_conversion_rate

        # 4. Cost of false positives (unnecessarily aggressive actions)
        cost_false_positives = fp * avg_booking_value * 0.05  # Minor cost per false alarm

        # 5. Cost of missed cancellations
        cost_missed = fn * avg_booking_value * 0.3  # Lost opportunity

        total_revenue_saved = revenue_overbooking + revenue_deposit + revenue_campaigns
        total_cost = cost_false_positives + cost_missed
        net_impact = total_revenue_saved - total_cost

        results[f"threshold_{threshold}"] = {
            "threshold": threshold,
            "true_positives": int(tp),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_negatives": int(tn),
            "precision": round(tp / max(tp + fp, 1), 4),
            "recall": round(tp / max(tp + fn, 1), 4),
            "revenue_saved_overbooking": round(revenue_overbooking, 2),
            "revenue_saved_deposits": round(revenue_deposit, 2),
            "revenue_saved_campaigns": round(revenue_campaigns, 2),
            "cost_false_positives": round(cost_false_positives, 2),
            "cost_missed_cancellations": round(cost_missed, 2),
            "net_revenue_impact": round(net_impact, 2),
        }

    # Find optimal threshold
    best_threshold = max(results, key=lambda k: results[k]["net_revenue_impact"])
    optimal = results[best_threshold]

    logger.info("\n" + "=" * 60)
    logger.info("  BUSINESS IMPACT ANALYSIS")
    logger.info("=" * 60)
    logger.info(f"  Average booking value: EUR {avg_booking_value:.2f}")
    logger.info(f"  Optimal threshold: {optimal['threshold']}")
    logger.info(f"  Net revenue impact: EUR {optimal['net_revenue_impact']:,.2f}")
    logger.info(f"  Revenue from overbooking: EUR {optimal['revenue_saved_overbooking']:,.2f}")
    logger.info(f"  Revenue from campaigns: EUR {optimal['revenue_saved_campaigns']:,.2f}")
    logger.info(f"  True positives: {optimal['true_positives']}")
    logger.info(f"  False positives: {optimal['false_positives']}")

    # Annualized estimate (test set is 20% of data)
    annual_factor = 5  # Approximate annualization from test set
    annual_impact = optimal["net_revenue_impact"] * annual_factor
    logger.info(f"\n  Estimated annual impact: EUR {annual_impact:,.2f}")

    return {
        "threshold_analysis": results,
        "optimal_threshold": optimal["threshold"],
        "net_annual_impact": round(annual_impact, 2),
        "avg_booking_value": round(avg_booking_value, 2),
    }


def find_optimal_threshold(y_test, y_proba) -> float:
    """Find threshold that maximizes F1 score."""
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[min(optimal_idx, len(thresholds) - 1)]
    logger.info(f"Optimal F1 threshold: {optimal_threshold:.3f} (F1: {f1_scores[optimal_idx]:.4f})")
    return optimal_threshold


def run_evaluation_pipeline(training_output: dict) -> dict:
    """Run complete evaluation pipeline."""
    logger.info("=" * 60)
    logger.info("  EVALUATION & BUSINESS IMPACT PIPELINE")
    logger.info("=" * 60)

    data = training_output["data"]
    best_name = training_output["best_model_name"]
    best_model = training_output["trained_models"][best_name]

    X_test = data["X_test"]
    y_test = data["y_test"]

    # Get probabilities
    if best_name == "Logistic Regression":
        scaler = training_output["trained_models"]["scaler"]
        X_test_input = pd.DataFrame(
            scaler.transform(X_test), columns=X_test.columns, index=X_test.index
        )
    else:
        X_test_input = X_test

    y_proba = best_model.predict_proba(X_test_input)[:, 1]

    # SHAP Analysis
    shap_results = compute_shap_values(best_model, X_test_input, best_name)

    # Optimal threshold
    optimal_threshold = find_optimal_threshold(y_test, y_proba)

    # Load original data for business impact (need ADR and nights)
    from src.module_1_predictive.cancellation.eda import load_data
    full_df = load_data()

    # Get ADR and nights for test set indices
    adr_values = full_df.loc[X_test.index, "adr"] if "adr" in full_df.columns else pd.Series([100] * len(X_test))
    nights_values = full_df.loc[X_test.index, "stays_in_week_nights"] + full_df.loc[X_test.index, "stays_in_weekend_nights"] if "stays_in_week_nights" in full_df.columns else pd.Series([3] * len(X_test))

    # Business impact
    business_impact = calculate_business_impact(y_test, y_proba, adr_values, nights_values)

    # Save evaluation results
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    eval_results = {
        "best_model": best_name,
        "optimal_f1_threshold": round(optimal_threshold, 3),
        "business_impact": business_impact,
    }

    if shap_results:
        feature_importance = shap_results["feature_importance"]
        feature_importance.to_csv(MODELS_DIR / "shap_feature_importance.csv")
        eval_results["top_features"] = feature_importance.head(20).to_dict()

    with open(MODELS_DIR / "evaluation_results.json", "w") as f:
        json.dump(eval_results, f, indent=2, default=str)

    logger.info(f"\nEvaluation results saved to {MODELS_DIR}")
    return eval_results


def main():
    from src.module_1_predictive.cancellation.eda import load_data
    from src.module_1_predictive.cancellation.features import run_feature_engineering
    from src.module_1_predictive.cancellation.train import run_training_pipeline

    df = load_data()
    df, feature_cols = run_feature_engineering(df)
    training_output = run_training_pipeline(df, feature_cols)
    run_evaluation_pipeline(training_output)


if __name__ == "__main__":
    main()
