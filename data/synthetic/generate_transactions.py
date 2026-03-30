"""
CLTV Transaction Data Generator

Generates synthetic hotel customer transaction history for BG-NBD and
Gamma-Gamma CLTV modeling. Produces 10,000+ customers with 2 years of
realistic booking and spending patterns.

Output: data/synthetic/transactions.csv
"""

import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()
Faker.seed(42)
np.random.seed(42)

OUTPUT_DIR = Path(__file__).parent
NUM_CUSTOMERS = 12000
DATE_START = datetime(2024, 1, 1)
DATE_END = datetime(2025, 12, 31)
DAYS_RANGE = (DATE_END - DATE_START).days


def generate_customer_profiles(n: int) -> pd.DataFrame:
    """Generate customer base with different behavioral segments."""
    segments = {
        "champion": {"pct": 0.08, "freq_range": (8, 20), "monetary_range": (200, 800)},
        "loyal": {"pct": 0.15, "freq_range": (5, 12), "monetary_range": (150, 500)},
        "potential": {"pct": 0.20, "freq_range": (3, 7), "monetary_range": (100, 350)},
        "at_risk": {"pct": 0.25, "freq_range": (2, 5), "monetary_range": (80, 250)},
        "lost": {"pct": 0.32, "freq_range": (1, 3), "monetary_range": (50, 200)},
    }

    customers = []
    customer_id = 1

    for seg_name, seg_params in segments.items():
        seg_count = int(n * seg_params["pct"])
        for _ in range(seg_count):
            customers.append({
                "customer_id": f"C{customer_id:05d}",
                "segment_true": seg_name,
                "expected_frequency": np.random.uniform(*seg_params["freq_range"]),
                "monetary_mean": np.random.uniform(*seg_params["monetary_range"]),
                "country": fake.country_code(representation="alpha-2"),
                "customer_type": np.random.choice(
                    ["Business", "Leisure", "Group", "Corporate"],
                    p=[0.25, 0.45, 0.15, 0.15],
                ),
            })
            customer_id += 1

    return pd.DataFrame(customers)


def generate_transactions(profiles: pd.DataFrame) -> pd.DataFrame:
    """Generate transaction records based on customer profiles."""
    transactions = []

    for _, customer in profiles.iterrows():
        n_transactions = max(1, int(np.random.poisson(customer["expected_frequency"])))

        # Champions and loyals start earlier
        if customer["segment_true"] in ("champion", "loyal"):
            first_date = DATE_START + timedelta(days=np.random.randint(0, 60))
        elif customer["segment_true"] == "potential":
            first_date = DATE_START + timedelta(days=np.random.randint(30, 180))
        elif customer["segment_true"] == "at_risk":
            first_date = DATE_START + timedelta(days=np.random.randint(0, 120))
            # At risk: last transaction is old
            n_transactions = min(n_transactions, 3)
        else:  # lost
            first_date = DATE_START + timedelta(days=np.random.randint(0, 90))
            n_transactions = min(n_transactions, 2)

        dates = sorted([
            first_date + timedelta(days=np.random.randint(0, DAYS_RANGE))
            for _ in range(n_transactions)
        ])

        # Lost customers: force last transaction to be old
        if customer["segment_true"] == "lost":
            dates = [d for d in dates if d < DATE_START + timedelta(days=365)]
            if not dates:
                dates = [first_date]

        for date in dates:
            # Monetary value with some noise
            base_amount = customer["monetary_mean"]
            amount = max(30, np.random.normal(base_amount, base_amount * 0.3))

            # Stay duration affects total
            nights = np.random.choice([1, 2, 3, 4, 5, 7, 10, 14],
                                       p=[0.10, 0.20, 0.25, 0.15, 0.10, 0.10, 0.05, 0.05])

            room_type = np.random.choice(
                ["Standard", "Superior", "Deluxe", "Suite", "Presidential"],
                p=[0.35, 0.30, 0.20, 0.12, 0.03],
            )

            # Room type multiplier
            multiplier = {
                "Standard": 1.0, "Superior": 1.3, "Deluxe": 1.7,
                "Suite": 2.5, "Presidential": 4.0,
            }[room_type]

            total_revenue = round(amount * nights * multiplier, 2)

            transactions.append({
                "transaction_id": f"T{len(transactions)+1:06d}",
                "customer_id": customer["customer_id"],
                "transaction_date": date.strftime("%Y-%m-%d"),
                "nights": nights,
                "room_type": room_type,
                "daily_rate": round(amount * multiplier, 2),
                "total_revenue": total_revenue,
                "hotel_type": np.random.choice(
                    ["Resort Hotel", "City Hotel"], p=[0.4, 0.6]
                ),
                "booking_channel": np.random.choice(
                    ["Direct", "OTA", "Corporate", "Travel Agent"],
                    p=[0.25, 0.40, 0.20, 0.15],
                ),
                "meal_plan": np.random.choice(
                    ["BB", "HB", "FB", "RO"],
                    p=[0.40, 0.30, 0.15, 0.15],
                ),
                "extra_spend": round(max(0, np.random.normal(50, 40)), 2),
            })

    return pd.DataFrame(transactions)


def main():
    print("Generating customer profiles...")
    profiles = generate_customer_profiles(NUM_CUSTOMERS)
    print(f"  -> {len(profiles)} customers created")

    print("Generating transactions...")
    transactions = generate_transactions(profiles)
    print(f"  -> {len(transactions)} transactions created")

    # Save
    profiles.to_csv(OUTPUT_DIR / "customer_profiles.csv", index=False)
    transactions.to_csv(OUTPUT_DIR / "transactions.csv", index=False)

    print(f"\nSaved to {OUTPUT_DIR}/")
    print(f"  customer_profiles.csv: {len(profiles)} rows")
    print(f"  transactions.csv: {len(transactions)} rows")

    # Quick stats
    print(f"\nSegment distribution:")
    print(profiles["segment_true"].value_counts().to_string())
    print(f"\nRevenue stats:")
    print(transactions["total_revenue"].describe().to_string())


if __name__ == "__main__":
    main()
