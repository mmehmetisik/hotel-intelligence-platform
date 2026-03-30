"""
Booking Cancellation — Feature Engineering

Creates predictive features from raw hotel booking data:
- Temporal features (season, weekend, lead time buckets)
- Customer behavior features (repeat guest, history)
- Booking features (deposit, changes, special requests)
- Price features (ADR deviation, total cost)
- Interaction features (cross-feature combinations)
- Aggregation features (historical rates)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent


def create_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based features."""
    # Total stay duration
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    df["is_weekend_stay"] = (df["stays_in_weekend_nights"] > 0).astype(int)

    # Season mapping
    season_map = {
        "January": "Winter", "February": "Winter", "March": "Spring",
        "April": "Spring", "May": "Spring", "June": "Summer",
        "July": "Summer", "August": "Summer", "September": "Fall",
        "October": "Fall", "November": "Fall", "December": "Winter",
    }
    df["season"] = df["arrival_date_month"].map(season_map)

    # Lead time buckets
    df["lead_time_bucket"] = pd.cut(
        df["lead_time"],
        bins=[-1, 7, 30, 90, 180, 365, float("inf")],
        labels=["last_minute", "short", "medium", "long", "very_long", "extreme"],
    )

    # Month number for cyclical encoding
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12,
    }
    df["arrival_month_num"] = df["arrival_date_month"].map(month_map)

    # Cyclical encoding
    df["arrival_month_sin"] = np.sin(2 * np.pi * df["arrival_month_num"] / 12)
    df["arrival_month_cos"] = np.cos(2 * np.pi * df["arrival_month_num"] / 12)

    logger.info("Temporal features created")
    return df


def create_customer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer behavior features."""
    # Total previous interactions
    df["total_previous_bookings"] = (
        df["previous_cancellations"] + df["previous_bookings_not_canceled"]
    )

    # Previous cancellation ratio (avoid division by zero)
    df["prev_cancel_ratio"] = np.where(
        df["total_previous_bookings"] > 0,
        df["previous_cancellations"] / df["total_previous_bookings"],
        0,
    )

    # Total guests
    df["total_guests"] = df["adults"] + df["children"] + df["babies"]
    df["has_children"] = (df["children"] > 0).astype(int)
    df["has_babies"] = (df["babies"] > 0).astype(int)
    df["is_solo"] = ((df["adults"] == 1) & (df["children"] == 0) & (df["babies"] == 0)).astype(int)

    logger.info("Customer features created")
    return df


def create_booking_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create booking-related features."""
    # Room type mismatch
    df["room_type_mismatch"] = (df["reserved_room_type"] != df["assigned_room_type"]).astype(int)

    # Has agent / company
    df["has_agent"] = (df["agent"] > 0).astype(int)
    df["has_company"] = (df["company"] > 0).astype(int)

    # Waiting list flag
    df["had_waiting"] = (df["days_in_waiting_list"] > 0).astype(int)

    # Special requests flag
    df["has_special_requests"] = (df["total_of_special_requests"] > 0).astype(int)

    # Parking request flag
    df["needs_parking"] = (df["required_car_parking_spaces"] > 0).astype(int)

    logger.info("Booking features created")
    return df


def create_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create price-related features."""
    # Total estimated cost
    df["total_cost"] = df["adr"] * df["total_nights"]

    # ADR deviation from hotel mean
    hotel_adr_mean = df.groupby("hotel")["adr"].transform("mean")
    df["adr_deviation"] = df["adr"] - hotel_adr_mean

    # ADR per person
    df["adr_per_person"] = np.where(
        df["total_guests"] > 0,
        df["adr"] / df["total_guests"],
        df["adr"],
    )

    # Price category
    df["price_category"] = pd.qcut(
        df["adr"].clip(lower=0.01),
        q=4,
        labels=["budget", "economy", "standard", "premium"],
        duplicates="drop",
    )

    logger.info("Price features created")
    return df


def create_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create interaction features between key variables."""
    # Lead time x deposit type
    df["lead_deposit_interaction"] = (
        df["lead_time"] * df["deposit_type"].map(
            {"No Deposit": 0, "Refundable": 1, "Non Refund": 2}
        ).fillna(0)
    )

    # Repeated guest x previous cancellations
    df["repeat_cancel_interaction"] = (
        df["is_repeated_guest"] * df["previous_cancellations"]
    )

    # Total nights x ADR
    df["stay_value"] = df["total_nights"] * df["adr"]

    # Lead time x special requests (commitment signal)
    df["lead_requests_interaction"] = df["lead_time"] * df["total_of_special_requests"]

    logger.info("Interaction features created")
    return df


def create_aggregation_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create historical aggregation features."""
    # Historical cancellation rate by market segment
    segment_cancel_rate = df.groupby("market_segment")["is_canceled"].transform("mean")
    df["segment_cancel_rate"] = segment_cancel_rate

    # Historical cancellation rate by hotel + month
    hotel_month_rate = df.groupby(
        ["hotel", "arrival_date_month"]
    )["is_canceled"].transform("mean")
    df["hotel_month_cancel_rate"] = hotel_month_rate

    # Historical cancellation rate by country
    country_cancel_rate = df.groupby("country")["is_canceled"].transform("mean")
    df["country_cancel_rate"] = country_cancel_rate

    # Historical cancellation rate by deposit type
    deposit_cancel_rate = df.groupby("deposit_type")["is_canceled"].transform("mean")
    df["deposit_cancel_rate"] = deposit_cancel_rate

    logger.info("Aggregation features created")
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical variables for modeling."""
    # Label encoding for ordinal-like features
    label_encode_cols = {
        "hotel": {"Resort Hotel": 0, "City Hotel": 1},
        "deposit_type": {"No Deposit": 0, "Refundable": 1, "Non Refund": 2},
        "meal": {"SC": 0, "Undefined": 0, "BB": 1, "HB": 2, "FB": 3},
    }
    for col, mapping in label_encode_cols.items():
        df[f"{col}_encoded"] = df[col].map(mapping).fillna(0).astype(int)

    # One-hot encoding for nominal features
    nominal_cols = ["customer_type", "market_segment", "distribution_channel", "season"]
    df = pd.get_dummies(df, columns=nominal_cols, drop_first=True, dtype=int)

    logger.info("Categorical encoding complete")
    return df


def get_feature_columns(df: pd.DataFrame) -> list:
    """Get the list of feature columns for modeling."""
    exclude_cols = {
        "is_canceled", "reservation_status", "reservation_status_date",
        "arrival_date_month", "country", "agent", "company",
        "hotel", "deposit_type", "meal", "assigned_room_type",
        "reserved_room_type", "lead_time_bucket", "price_category",
        "arrival_date_year", "arrival_date_week_number", "arrival_date_day_of_month",
    }
    feature_cols = [
        col for col in df.columns
        if col not in exclude_cols
        and df[col].dtype in [np.int64, np.float64, np.int32, np.float32, int, float, np.uint8]
    ]
    logger.info(f"Selected {len(feature_cols)} features for modeling")
    return feature_cols


def run_feature_engineering(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Run the full feature engineering pipeline."""
    logger.info("=" * 60)
    logger.info("  FEATURE ENGINEERING PIPELINE")
    logger.info("=" * 60)

    df = create_temporal_features(df)
    df = create_customer_features(df)
    df = create_booking_features(df)
    df = create_price_features(df)
    df = create_interaction_features(df)
    df = create_aggregation_features(df)
    df = encode_categoricals(df)

    feature_cols = get_feature_columns(df)

    logger.info(f"\nFinal dataset: {df.shape}")
    logger.info(f"Feature count: {len(feature_cols)}")

    return df, feature_cols


def main():
    from src.module_1_predictive.cancellation.eda import load_data

    df = load_data()
    df, feature_cols = run_feature_engineering(df)

    # Save
    output_dir = ROOT_DIR / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "bookings_featured.csv", index=False)

    with open(output_dir / "feature_columns.txt", "w") as f:
        f.write("\n".join(feature_cols))

    logger.info(f"Saved featured dataset and {len(feature_cols)} feature names")


if __name__ == "__main__":
    main()
