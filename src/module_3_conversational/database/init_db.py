"""
Database Initialization

Creates SQLite database and loads synthetic data for the
Conversational AI module to query.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
DB_PATH = ROOT_DIR / "data" / "hotel.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
SYNTHETIC_DIR = ROOT_DIR / "data" / "synthetic"
RAW_DIR = ROOT_DIR / "data" / "raw"


def create_database():
    """Create database and tables from schema."""
    conn = sqlite3.connect(str(DB_PATH))
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())
    logger.info(f"Database created: {DB_PATH}")
    return conn


def load_bookings(conn: sqlite3.Connection):
    """Load hotel bookings data."""
    csv_path = RAW_DIR / "hotel_bookings.csv"
    if not csv_path.exists():
        logger.warning(f"Bookings CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    # Create arrival_date column
    df["arrival_date"] = pd.to_datetime(
        df["arrival_date_year"].astype(str) + "-" +
        df["arrival_date_month"] + "-" +
        df["arrival_date_day_of_month"].astype(str),
        format="%Y-%B-%d",
    ).dt.strftime("%Y-%m-%d")

    df["booking_id"] = [f"B{i:06d}" for i in range(len(df))]

    cols = [
        "booking_id", "hotel", "is_canceled", "lead_time", "arrival_date",
        "arrival_date_year", "arrival_date_month",
        "stays_in_weekend_nights", "stays_in_week_nights",
        "adults", "children", "babies", "meal", "country",
        "market_segment", "distribution_channel", "is_repeated_guest",
        "previous_cancellations", "previous_bookings_not_canceled",
        "deposit_type", "customer_type", "adr",
        "required_car_parking_spaces", "total_of_special_requests",
        "reservation_status",
    ]
    df[cols].to_sql("bookings", conn, if_exists="replace", index=False)
    logger.info(f"  Loaded {len(df)} bookings")


def load_transactions(conn: sqlite3.Connection):
    """Load transaction data."""
    csv_path = SYNTHETIC_DIR / "transactions.csv"
    if not csv_path.exists():
        logger.warning(f"Transactions CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    logger.info(f"  Loaded {len(df)} transactions")


def load_customers(conn: sqlite3.Connection):
    """Load customer profiles."""
    csv_path = SYNTHETIC_DIR / "customer_profiles.csv"
    if not csv_path.exists():
        logger.warning(f"Customer profiles CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    cols = ["customer_id", "country", "customer_type", "segment_true"]
    df[cols].to_sql("customers", conn, if_exists="replace", index=False)
    logger.info(f"  Loaded {len(df)} customers")


def load_reviews(conn: sqlite3.Connection):
    """Load review data."""
    csv_path = SYNTHETIC_DIR / "reviews.csv"
    if not csv_path.exists():
        logger.warning(f"Reviews CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df.to_sql("reviews", conn, if_exists="replace", index=False)
    logger.info(f"  Loaded {len(df)} reviews")


def load_customer_segments(conn: sqlite3.Connection):
    """Load CLTV/RFM segment data if available."""
    csv_path = ROOT_DIR / "data" / "processed" / "customers_cltv.csv"
    if not csv_path.exists():
        logger.info("  CLTV data not found (run CLTV pipeline first)")
        return

    df = pd.read_csv(csv_path)
    segment_df = df[["customer_id", "recency", "frequency", "monetary",
                      "total_revenue", "R_score", "F_score", "M_score",
                      "RFM_score", "rfm_segment"]].copy()

    if "cltv_6m" in df.columns:
        segment_df["cltv"] = df["cltv_6m"]
    else:
        segment_df["cltv"] = 0

    if "cltv_segment" in df.columns:
        segment_df["segment"] = df["cltv_segment"]
    else:
        segment_df["segment"] = df["rfm_segment"]

    segment_df.to_sql("customer_segments", conn, if_exists="replace", index=False)
    logger.info(f"  Loaded {len(segment_df)} customer segments")


def initialize_database() -> sqlite3.Connection:
    """Full database initialization pipeline."""
    logger.info("=" * 60)
    logger.info("  DATABASE INITIALIZATION")
    logger.info("=" * 60)

    conn = create_database()

    logger.info("\nLoading data...")
    load_bookings(conn)
    load_transactions(conn)
    load_customers(conn)
    load_reviews(conn)
    load_customer_segments(conn)

    conn.commit()

    # Verify
    cursor = conn.cursor()
    for table in ["bookings", "transactions", "customers", "reviews", "customer_segments"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        logger.info(f"  {table}: {count} rows")

    logger.info(f"\nDatabase ready: {DB_PATH}")
    return conn


def get_connection() -> sqlite3.Connection:
    """Get database connection, initializing if needed."""
    if not DB_PATH.exists():
        return initialize_database()
    return sqlite3.connect(str(DB_PATH))


def get_schema_description() -> str:
    """Get human-readable schema description for LLM context."""
    return """
DATABASE SCHEMA:

Table: bookings (hotel reservation data)
- booking_id, hotel (Resort Hotel/City Hotel), is_canceled (0/1)
- lead_time (days before arrival), arrival_date, arrival_date_year, arrival_date_month
- stays_in_weekend_nights, stays_in_week_nights, adults, children, babies
- meal (BB/HB/FB/SC), country, market_segment, distribution_channel
- is_repeated_guest, previous_cancellations, previous_bookings_not_canceled
- deposit_type, customer_type, adr (average daily rate)
- required_car_parking_spaces, total_of_special_requests, reservation_status

Table: transactions (customer spending data)
- transaction_id, customer_id, transaction_date, nights
- room_type (Standard/Superior/Deluxe/Suite/Presidential)
- daily_rate, total_revenue, hotel_type, booking_channel, meal_plan, extra_spend

Table: customers (customer profiles)
- customer_id, country, customer_type, segment_true

Table: customer_segments (RFM and CLTV scores)
- customer_id, recency, frequency, monetary, total_revenue
- R_score, F_score, M_score, RFM_score, rfm_segment, cltv, segment

Table: reviews (guest feedback)
- review_id, hotel, date, reviewer_country, trip_type
- rating (1-5), review_text, sentiment_true
- aspect_cleanliness, aspect_staff, aspect_food, aspect_location, aspect_value (1-5 each)
""".strip()


if __name__ == "__main__":
    initialize_database()
