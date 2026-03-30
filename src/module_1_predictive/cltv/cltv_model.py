"""
CLTV — BG-NBD + Gamma-Gamma Model Pipeline

Probabilistic Customer Lifetime Value calculation:
1. BG-NBD model: predicts future transaction frequency
2. Gamma-Gamma model: predicts average transaction value
3. CLTV = BG-NBD predicted frequency x Gamma-Gamma predicted value
4. Customer segmentation based on CLTV scores
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

ROOT_DIR = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = ROOT_DIR / "data" / "processed"
MODELS_DIR = ROOT_DIR / "models" / "cltv"


def fit_bgnbd_model(rfm: pd.DataFrame) -> tuple:
    """
    Fit BG-NBD model to predict future purchase frequency.

    Uses btyd library (active fork of lifetimes).
    Falls back to a simplified frequency-based approach if btyd is unavailable.
    """
    # Filter customers with repeat purchases for modeling
    rfm_model = rfm[rfm["frequency_repeat"] > 0].copy()

    try:
        from btyd import BetaGeoFitter

        bgf = BetaGeoFitter(penalizer_coef=0.01)
        bgf.fit(
            rfm_model["frequency_repeat"],
            rfm_model["recency"],
            rfm_model["T"],
        )

        logger.info("BG-NBD Model Parameters:")
        logger.info(f"  r: {bgf.params_['r']:.4f}")
        logger.info(f"  alpha: {bgf.params_['alpha']:.4f}")
        logger.info(f"  a: {bgf.params_['a']:.4f}")
        logger.info(f"  b: {bgf.params_['b']:.4f}")

        # Predict expected purchases in next 6 months (180 days)
        rfm["predicted_purchases_6m"] = bgf.conditional_expected_number_of_purchases_up_to_time(
            180,
            rfm["frequency_repeat"],
            rfm["recency"],
            rfm["T"],
        )

        # Predict probability of being alive
        rfm["prob_alive"] = bgf.conditional_probability_alive(
            rfm["frequency_repeat"],
            rfm["recency"],
            rfm["T"],
        )

        logger.info(f"BG-NBD fitted successfully on {len(rfm_model)} customers")
        return rfm, bgf

    except ImportError:
        logger.warning("btyd not installed. Using frequency-based fallback.")
        # Simplified fallback
        avg_freq = rfm["frequency_repeat"].mean()
        rfm["predicted_purchases_6m"] = (
            rfm["frequency_repeat"] / rfm["T"].clip(lower=1) * 180
        ).clip(lower=0)
        rfm["prob_alive"] = np.where(rfm["recency"] < 180, 0.8, 0.3)
        return rfm, None


def fit_gamma_gamma_model(rfm: pd.DataFrame) -> tuple:
    """
    Fit Gamma-Gamma model to predict average transaction value.
    """
    rfm_model = rfm[rfm["frequency_repeat"] > 0].copy()

    try:
        from btyd import GammaGammaFitter

        ggf = GammaGammaFitter(penalizer_coef=0.01)
        ggf.fit(
            rfm_model["frequency_repeat"],
            rfm_model["monetary"],
        )

        logger.info("Gamma-Gamma Model Parameters:")
        logger.info(f"  p: {ggf.params_['p']:.4f}")
        logger.info(f"  q: {ggf.params_['q']:.4f}")
        logger.info(f"  v: {ggf.params_['v']:.4f}")

        # Predict expected average profit
        rfm["predicted_monetary"] = ggf.conditional_expected_average_profit(
            rfm["frequency_repeat"],
            rfm["monetary"],
        )

        # Handle customers with 0 repeat (use their actual monetary value)
        rfm.loc[rfm["frequency_repeat"] == 0, "predicted_monetary"] = rfm.loc[
            rfm["frequency_repeat"] == 0, "monetary"
        ]

        logger.info(f"Gamma-Gamma fitted successfully")
        return rfm, ggf

    except ImportError:
        logger.warning("btyd not installed. Using monetary mean fallback.")
        rfm["predicted_monetary"] = rfm["monetary"]
        return rfm, None


def calculate_cltv(rfm: pd.DataFrame, months: int = 6) -> pd.DataFrame:
    """
    Calculate Customer Lifetime Value.

    CLTV = predicted_purchases x predicted_monetary x profit_margin
    """
    profit_margin = 0.35  # Hotel industry typical margin

    rfm["cltv_6m"] = (
        rfm["predicted_purchases_6m"]
        * rfm["predicted_monetary"]
        * profit_margin
    ).round(2)

    # Normalize to 0-100 scale for easier interpretation
    rfm["cltv_score"] = (
        (rfm["cltv_6m"] - rfm["cltv_6m"].min())
        / (rfm["cltv_6m"].max() - rfm["cltv_6m"].min())
        * 100
    ).round(1)

    logger.info(f"\nCLTV Statistics:")
    logger.info(f"  Mean CLTV (6m): EUR {rfm['cltv_6m'].mean():.2f}")
    logger.info(f"  Median CLTV (6m): EUR {rfm['cltv_6m'].median():.2f}")
    logger.info(f"  Max CLTV (6m): EUR {rfm['cltv_6m'].max():.2f}")
    logger.info(f"  Total predicted value: EUR {rfm['cltv_6m'].sum():,.2f}")

    return rfm


def segment_customers(rfm: pd.DataFrame) -> pd.DataFrame:
    """Segment customers based on CLTV scores."""
    rfm["cltv_segment"] = pd.qcut(
        rfm["cltv_score"].rank(method="first"),
        q=4,
        labels=["Low Value", "Medium Value", "High Value", "Premium"],
    )

    # More granular segmentation combining CLTV + recency
    conditions = [
        (rfm["cltv_segment"] == "Premium") & (rfm["prob_alive"] > 0.6),
        (rfm["cltv_segment"] == "Premium") & (rfm["prob_alive"] <= 0.6),
        (rfm["cltv_segment"] == "High Value") & (rfm["prob_alive"] > 0.5),
        (rfm["cltv_segment"].isin(["High Value", "Medium Value"])) & (rfm["prob_alive"] <= 0.4),
        (rfm["cltv_segment"] == "Low Value") & (rfm["prob_alive"] > 0.5),
        (rfm["cltv_segment"] == "Low Value") & (rfm["prob_alive"] <= 0.5),
    ]
    choices = [
        "VIP Active", "VIP At Risk", "Growing",
        "Declining", "New/Low", "Churned"
    ]
    rfm["action_segment"] = np.select(conditions, choices, default="Standard")

    logger.info(f"\nCLTV Segments:")
    logger.info(rfm["cltv_segment"].value_counts().to_string())
    logger.info(f"\nAction Segments:")
    logger.info(rfm["action_segment"].value_counts().to_string())

    # Business recommendations per segment
    recommendations = {
        "VIP Active": "Exclusive loyalty rewards, personal concierge, early access to promotions",
        "VIP At Risk": "URGENT: Personal outreach, win-back offer, satisfaction survey",
        "Growing": "Upgrade offers, loyalty program enrollment, cross-sell spa/dining",
        "Declining": "Re-engagement campaign, special discount, feedback request",
        "New/Low": "Welcome sequence, first-stay discount on return, newsletter",
        "Churned": "Win-back email series, significant discount offer",
        "Standard": "Regular marketing, seasonal promotions",
    }

    rfm["recommendation"] = rfm["action_segment"].map(recommendations)

    return rfm


def save_cltv_results(rfm: pd.DataFrame, bgf, ggf):
    """Save all CLTV results."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Save customer CLTV table
    rfm.to_csv(OUTPUT_DIR / "customers_cltv.csv", index=False)

    # Save models
    if bgf is not None:
        import joblib
        joblib.dump(bgf, MODELS_DIR / "bgnbd_model.joblib")
    if ggf is not None:
        import joblib
        joblib.dump(ggf, MODELS_DIR / "gamma_gamma_model.joblib")

    # Save summary stats
    summary = {
        "total_customers": len(rfm),
        "mean_cltv_6m": round(rfm["cltv_6m"].mean(), 2),
        "median_cltv_6m": round(rfm["cltv_6m"].median(), 2),
        "total_predicted_value_6m": round(rfm["cltv_6m"].sum(), 2),
        "segment_summary": rfm.groupby("cltv_segment")["cltv_6m"].agg(
            ["count", "mean", "sum"]
        ).round(2).to_dict(),
        "action_segment_counts": rfm["action_segment"].value_counts().to_dict(),
        "avg_prob_alive": round(rfm["prob_alive"].mean(), 4),
    }

    with open(MODELS_DIR / "cltv_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    logger.info(f"CLTV results saved to {OUTPUT_DIR} and {MODELS_DIR}")


def run_cltv_pipeline() -> pd.DataFrame:
    """Run the complete CLTV pipeline."""
    logger.info("=" * 60)
    logger.info("  CLTV PIPELINE (BG-NBD + Gamma-Gamma)")
    logger.info("=" * 60)

    # Step 1: Prepare RFM data
    from src.module_1_predictive.cltv.data_prep import load_transactions, create_rfm_table, score_rfm

    transactions = load_transactions()
    rfm = create_rfm_table(transactions)
    rfm = score_rfm(rfm)

    # Step 2: BG-NBD (frequency prediction)
    logger.info("\n--- BG-NBD Model ---")
    rfm, bgf = fit_bgnbd_model(rfm)

    # Step 3: Gamma-Gamma (monetary prediction)
    logger.info("\n--- Gamma-Gamma Model ---")
    rfm, ggf = fit_gamma_gamma_model(rfm)

    # Step 4: Calculate CLTV
    logger.info("\n--- CLTV Calculation ---")
    rfm = calculate_cltv(rfm)

    # Step 5: Segment customers
    logger.info("\n--- Customer Segmentation ---")
    rfm = segment_customers(rfm)

    # Step 6: Save
    save_cltv_results(rfm, bgf, ggf)

    return rfm


def main():
    run_cltv_pipeline()


if __name__ == "__main__":
    main()
