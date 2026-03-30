"""
Customer Segmentation — Feature Engineering

Creates behavioral features from booking and transaction data
for unsupervised clustering and supervised classification.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent


def create_clustering_features() -> pd.DataFrame:
    """
    Create feature matrix for customer segmentation.

    Combines transaction patterns, booking preferences,
    and spending behavior into a unified feature set.
    """
    # Load transaction data
    transactions = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "transactions.csv")
    transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
    profiles = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "customer_profiles.csv")

    analysis_date = pd.to_datetime("2026-01-01")

    # Aggregate per customer
    customer_features = transactions.groupby("customer_id").agg(
        # Recency & Frequency
        recency=("transaction_date", lambda x: (analysis_date - x.max()).days),
        frequency=("transaction_id", "count"),
        tenure_days=("transaction_date", lambda x: (analysis_date - x.min()).days),

        # Monetary
        total_revenue=("total_revenue", "sum"),
        avg_revenue=("total_revenue", "mean"),
        std_revenue=("total_revenue", "std"),
        max_revenue=("total_revenue", "max"),
        min_revenue=("total_revenue", "min"),

        # Stay patterns
        avg_nights=("nights", "mean"),
        total_nights=("nights", "sum"),
        max_nights=("nights", "max"),

        # Rate
        avg_daily_rate=("daily_rate", "mean"),

        # Extra spending
        avg_extra_spend=("extra_spend", "mean"),
        total_extra_spend=("extra_spend", "sum"),
    ).reset_index()

    # Fill NaN in std (single transaction customers)
    customer_features["std_revenue"] = customer_features["std_revenue"].fillna(0)

    # Derived features
    customer_features["revenue_per_night"] = (
        customer_features["total_revenue"] / customer_features["total_nights"].clip(lower=1)
    )
    customer_features["booking_frequency"] = (
        customer_features["frequency"] / customer_features["tenure_days"].clip(lower=1) * 365
    )  # Annualized booking frequency
    customer_features["revenue_consistency"] = (
        1 - customer_features["std_revenue"] / customer_features["avg_revenue"].clip(lower=1)
    ).clip(lower=0, upper=1)

    # Room type preferences (one-hot encoded mode)
    room_mode = transactions.groupby("customer_id")["room_type"].agg(
        lambda x: x.mode().iloc[0]
    ).reset_index()
    room_dummies = pd.get_dummies(room_mode["room_type"], prefix="pref_room", dtype=int)
    room_mode = pd.concat([room_mode[["customer_id"]], room_dummies], axis=1)
    customer_features = customer_features.merge(room_mode, on="customer_id", how="left")

    # Channel preference
    channel_mode = transactions.groupby("customer_id")["booking_channel"].agg(
        lambda x: x.mode().iloc[0]
    ).reset_index()
    channel_dummies = pd.get_dummies(channel_mode["booking_channel"], prefix="pref_channel", dtype=int)
    channel_mode = pd.concat([channel_mode[["customer_id"]], channel_dummies], axis=1)
    customer_features = customer_features.merge(channel_mode, on="customer_id", how="left")

    # Hotel type preference
    hotel_pref = transactions.groupby("customer_id")["hotel_type"].agg(
        lambda x: (x == "Resort Hotel").mean()
    ).reset_index()
    hotel_pref.columns = ["customer_id", "resort_ratio"]
    customer_features = customer_features.merge(hotel_pref, on="customer_id", how="left")

    # Merge true segment from profiles (for evaluation)
    customer_features = customer_features.merge(
        profiles[["customer_id", "segment_true", "customer_type"]],
        on="customer_id",
        how="left",
    )

    logger.info(f"Clustering features: {customer_features.shape}")
    logger.info(f"Features per customer: {customer_features.shape[1] - 2}")  # minus id and true segment

    return customer_features


def main():
    features = create_clustering_features()
    output_dir = ROOT_DIR / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_dir / "customer_clustering_features.csv", index=False)
    logger.info(f"Saved {len(features)} customer feature records")


if __name__ == "__main__":
    main()
