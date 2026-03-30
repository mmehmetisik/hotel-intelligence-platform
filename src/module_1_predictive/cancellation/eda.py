"""
Booking Cancellation — Exploratory Data Analysis

Comprehensive EDA on Hotel Booking Demand dataset:
- Data overview and quality checks
- Target variable distribution
- Feature distributions and correlations
- Key insights for feature engineering
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
DATA_PATH = ROOT_DIR / "data" / "raw" / "hotel_bookings.csv"
OUTPUT_DIR = ROOT_DIR / "data" / "processed"


def load_data() -> pd.DataFrame:
    """Load and perform initial cleaning of hotel bookings data."""
    logger.info(f"Loading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # Basic cleaning
    df["children"] = df["children"].fillna(0)
    df["country"] = df["country"].fillna("Unknown")
    df["agent"] = df["agent"].fillna(0).astype(int)
    df["company"] = df["company"].fillna(0).astype(int)

    # Remove rows with 0 guests
    mask = (df["adults"] + df["children"] + df["babies"]) > 0
    removed = (~mask).sum()
    df = df[mask].reset_index(drop=True)
    if removed > 0:
        logger.info(f"Removed {removed} rows with 0 guests")

    # Remove negative ADR
    neg_adr = (df["adr"] < 0).sum()
    df = df[df["adr"] >= 0].reset_index(drop=True)
    if neg_adr > 0:
        logger.info(f"Removed {neg_adr} rows with negative ADR")

    return df


def data_overview(df: pd.DataFrame) -> dict:
    """Generate data overview statistics."""
    overview = {
        "shape": df.shape,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2),
        "cancellation_rate": df["is_canceled"].mean() * 100,
        "hotel_distribution": df["hotel"].value_counts().to_dict(),
        "numeric_stats": df.describe(),
    }
    logger.info(f"Cancellation rate: {overview['cancellation_rate']:.1f}%")
    return overview


def analyze_cancellation_patterns(df: pd.DataFrame) -> dict:
    """Analyze cancellation patterns across key dimensions."""
    patterns = {}

    # By hotel type
    patterns["by_hotel"] = df.groupby("hotel")["is_canceled"].mean().round(4)

    # By lead time buckets
    df["lead_time_bucket"] = pd.cut(
        df["lead_time"],
        bins=[0, 7, 30, 90, 180, 365, float("inf")],
        labels=["0-7d", "8-30d", "31-90d", "91-180d", "181-365d", "365d+"],
    )
    patterns["by_lead_time"] = df.groupby("lead_time_bucket", observed=True)["is_canceled"].mean().round(4)

    # By deposit type
    patterns["by_deposit"] = df.groupby("deposit_type")["is_canceled"].mean().round(4)

    # By customer type
    patterns["by_customer_type"] = df.groupby("customer_type")["is_canceled"].mean().round(4)

    # By market segment
    patterns["by_market_segment"] = df.groupby("market_segment")["is_canceled"].mean().round(4)

    # By month
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    patterns["by_month"] = (
        df.groupby("arrival_date_month")["is_canceled"]
        .mean()
        .reindex(month_order)
        .round(4)
    )

    # By repeated guest
    patterns["by_repeated_guest"] = df.groupby("is_repeated_guest")["is_canceled"].mean().round(4)

    # By special requests
    patterns["by_special_requests"] = df.groupby("total_of_special_requests")["is_canceled"].mean().round(4)

    for key, val in patterns.items():
        logger.info(f"\nCancellation rate {key}:\n{val}")

    return patterns


def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute correlations with target variable."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()["is_canceled"].drop("is_canceled").sort_values(ascending=False)
    logger.info(f"\nTop correlations with cancellation:\n{correlations.head(10)}")
    return correlations


def generate_eda_report(df: pd.DataFrame) -> dict:
    """Run complete EDA pipeline and return all results."""
    logger.info("=" * 60)
    logger.info("  BOOKING CANCELLATION — EDA REPORT")
    logger.info("=" * 60)

    overview = data_overview(df)
    patterns = analyze_cancellation_patterns(df)
    correlations = correlation_analysis(df)

    report = {
        "overview": overview,
        "patterns": patterns,
        "correlations": correlations,
        "dataframe": df,
    }

    logger.info("\nEDA complete.")
    return report


def main():
    df = load_data()
    report = generate_eda_report(df)

    # Save cleaned data
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / "hotel_bookings_cleaned.csv", index=False)
    logger.info(f"Cleaned data saved: {len(df)} rows")


if __name__ == "__main__":
    main()
