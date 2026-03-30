"""
CLTV — Data Preparation

Prepares transaction data for RFM analysis and probabilistic
CLTV models (BG-NBD + Gamma-Gamma).
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "data" / "synthetic"


def load_transactions() -> pd.DataFrame:
    """Load and validate transaction data."""
    df = pd.read_csv(DATA_DIR / "transactions.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    logger.info(f"Loaded {len(df)} transactions, {df['customer_id'].nunique()} customers")
    return df


def create_rfm_table(df: pd.DataFrame, analysis_date: str = "2026-01-01") -> pd.DataFrame:
    """
    Create RFM (Recency, Frequency, Monetary) table.

    Args:
        df: Transaction dataframe
        analysis_date: Reference date for recency calculation

    Returns:
        RFM table with one row per customer
    """
    analysis_date = pd.to_datetime(analysis_date)

    rfm = df.groupby("customer_id").agg(
        recency=("transaction_date", lambda x: (analysis_date - x.max()).days),
        frequency=("transaction_id", "count"),
        monetary=("total_revenue", "mean"),
        total_revenue=("total_revenue", "sum"),
        first_purchase=("transaction_date", "min"),
        last_purchase=("transaction_date", "max"),
        avg_nights=("nights", "mean"),
        preferred_room=("room_type", lambda x: x.mode().iloc[0] if len(x) > 0 else "Unknown"),
        preferred_channel=("booking_channel", lambda x: x.mode().iloc[0] if len(x) > 0 else "Unknown"),
    ).reset_index()

    # T: customer's age in days (time since first purchase)
    rfm["T"] = (analysis_date - rfm["first_purchase"]).dt.days

    # For BG-NBD: frequency must be > 0 and represent repeat purchases
    # frequency = number of repeat purchases (total purchases - 1)
    rfm["frequency_repeat"] = rfm["frequency"] - 1

    logger.info(f"RFM table: {len(rfm)} customers")
    logger.info(f"  Recency — mean: {rfm['recency'].mean():.0f}, median: {rfm['recency'].median():.0f}")
    logger.info(f"  Frequency — mean: {rfm['frequency'].mean():.1f}, median: {rfm['frequency'].median():.0f}")
    logger.info(f"  Monetary — mean: {rfm['monetary'].mean():.2f}, median: {rfm['monetary'].median():.2f}")

    return rfm


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign RFM scores (1-5) based on quintiles."""
    # Recency: lower is better (more recent) -> invert scoring
    rfm["R_score"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)

    # Frequency: higher is better
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    # Monetary: higher is better
    rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    # Combined RFM score
    rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

    # RFM segment label
    rfm["rfm_segment"] = rfm.apply(_assign_rfm_segment, axis=1)

    logger.info(f"\nRFM Segment distribution:")
    logger.info(rfm["rfm_segment"].value_counts().to_string())

    return rfm


def _assign_rfm_segment(row) -> str:
    """Assign customer segment based on RFM scores."""
    r, f, m = row["R_score"], row["F_score"], row["M_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champion"
    elif r >= 3 and f >= 3 and m >= 3:
        return "Loyal"
    elif r >= 4 and f <= 2:
        return "New Customer"
    elif r >= 3 and f >= 2:
        return "Potential Loyalist"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f >= 4 and m >= 4:
        return "Cant Lose"
    elif r <= 2 and f <= 2:
        return "Lost"
    elif r == 3 and f <= 2:
        return "About to Sleep"
    else:
        return "Need Attention"


def main():
    df = load_transactions()
    rfm = create_rfm_table(df)
    rfm = score_rfm(rfm)

    output_dir = ROOT_DIR / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(output_dir / "customers_rfm.csv", index=False)
    logger.info(f"Saved RFM table: {len(rfm)} customers")
    return rfm


if __name__ == "__main__":
    main()
