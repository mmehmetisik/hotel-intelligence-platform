"""
Data Quality Tests

Validates that all synthetic datasets meet expected quality standards:
row counts, column presence, value ranges, no critical nulls.
"""

import pandas as pd
import pytest
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "synthetic"


# ---------- Fixtures ----------

@pytest.fixture
def transactions():
    return pd.read_csv(DATA_DIR / "transactions.csv")


@pytest.fixture
def customer_profiles():
    return pd.read_csv(DATA_DIR / "customer_profiles.csv")


@pytest.fixture
def invoices():
    return pd.read_csv(DATA_DIR / "invoices.csv")


@pytest.fixture
def master_items():
    return pd.read_csv(DATA_DIR / "master_items.csv")


@pytest.fixture
def reviews():
    return pd.read_csv(DATA_DIR / "reviews.csv")


@pytest.fixture
def analytics_qa():
    return pd.read_csv(DATA_DIR / "analytics_qa.csv")


# ---------- Transaction Data Tests ----------

class TestTransactions:
    def test_min_row_count(self, transactions):
        assert len(transactions) >= 10000, "Need at least 10K transactions"

    def test_required_columns(self, transactions):
        required = [
            "transaction_id", "customer_id", "transaction_date",
            "nights", "room_type", "daily_rate", "total_revenue",
        ]
        for col in required:
            assert col in transactions.columns, f"Missing column: {col}"

    def test_no_null_ids(self, transactions):
        assert transactions["transaction_id"].notna().all()
        assert transactions["customer_id"].notna().all()

    def test_positive_revenue(self, transactions):
        assert (transactions["total_revenue"] > 0).all()

    def test_positive_nights(self, transactions):
        assert (transactions["nights"] > 0).all()

    def test_valid_room_types(self, transactions):
        valid = {"Standard", "Superior", "Deluxe", "Suite", "Presidential"}
        actual = set(transactions["room_type"].unique())
        assert actual.issubset(valid)

    def test_valid_dates(self, transactions):
        dates = pd.to_datetime(transactions["transaction_date"])
        assert dates.min() >= pd.Timestamp("2024-01-01")
        assert dates.max() <= pd.Timestamp("2026-12-31")

    def test_unique_transaction_ids(self, transactions):
        assert transactions["transaction_id"].is_unique


# ---------- Customer Profiles Tests ----------

class TestCustomerProfiles:
    def test_min_customers(self, customer_profiles):
        assert len(customer_profiles) >= 10000

    def test_segment_values(self, customer_profiles):
        valid = {"champion", "loyal", "potential", "at_risk", "lost"}
        actual = set(customer_profiles["segment_true"].unique())
        assert actual == valid

    def test_no_null_ids(self, customer_profiles):
        assert customer_profiles["customer_id"].notna().all()

    def test_unique_customer_ids(self, customer_profiles):
        assert customer_profiles["customer_id"].is_unique


# ---------- Invoice Data Tests ----------

class TestInvoices:
    def test_min_row_count(self, invoices):
        assert len(invoices) >= 5000

    def test_required_columns(self, invoices):
        required = ["invoice_id", "date", "description", "amount", "category_true"]
        for col in required:
            assert col in invoices.columns, f"Missing column: {col}"

    def test_no_empty_descriptions(self, invoices):
        assert (invoices["description"].str.len() > 0).all()

    def test_positive_amounts(self, invoices):
        assert (invoices["amount"] > 0).all()

    def test_valid_categories(self, invoices):
        expected_count = 8
        assert invoices["category_true"].nunique() == expected_count

    def test_valid_currencies(self, invoices):
        valid = {"EUR", "USD", "GBP"}
        actual = set(invoices["currency"].unique())
        assert actual.issubset(valid)


# ---------- Master Items Tests ----------

class TestMasterItems:
    def test_min_row_count(self, master_items):
        assert len(master_items) >= 1000

    def test_required_columns(self, master_items):
        required = ["item_id", "dirty_name", "standard_name", "category"]
        for col in required:
            assert col in master_items.columns

    def test_no_empty_names(self, master_items):
        assert (master_items["dirty_name"].str.strip().str.len() > 0).all()
        assert (master_items["standard_name"].str.strip().str.len() > 0).all()

    def test_multiple_standards(self, master_items):
        assert master_items["standard_name"].nunique() >= 20

    def test_valid_categories(self, master_items):
        valid = {"Beverage", "Food", "Spa", "Service"}
        actual = set(master_items["category"].unique())
        assert actual == valid


# ---------- Reviews Tests ----------

class TestReviews:
    def test_min_row_count(self, reviews):
        assert len(reviews) >= 2000

    def test_required_columns(self, reviews):
        required = [
            "review_id", "hotel", "date", "rating",
            "review_text", "sentiment_true",
        ]
        for col in required:
            assert col in reviews.columns

    def test_rating_range(self, reviews):
        assert reviews["rating"].between(1, 5).all()

    def test_sentiment_values(self, reviews):
        valid = {"positive", "mixed", "negative"}
        actual = set(reviews["sentiment_true"].unique())
        assert actual == valid

    def test_no_empty_reviews(self, reviews):
        assert (reviews["review_text"].str.len() > 10).all()

    def test_aspect_columns_exist(self, reviews):
        aspects = ["aspect_cleanliness", "aspect_staff", "aspect_food",
                    "aspect_location", "aspect_value"]
        for col in aspects:
            assert col in reviews.columns

    def test_aspect_ranges(self, reviews):
        aspects = ["aspect_cleanliness", "aspect_staff", "aspect_food",
                    "aspect_location", "aspect_value"]
        for col in aspects:
            assert reviews[col].between(1, 5).all()


# ---------- Analytics Q&A Tests ----------

class TestAnalyticsQA:
    def test_min_qa_count(self, analytics_qa):
        assert len(analytics_qa) >= 50

    def test_required_columns(self, analytics_qa):
        required = ["question", "intent", "expected_viz", "category"]
        for col in required:
            assert col in analytics_qa.columns

    def test_unique_questions(self, analytics_qa):
        assert analytics_qa["question"].is_unique

    def test_no_empty_questions(self, analytics_qa):
        assert (analytics_qa["question"].str.len() > 10).all()

    def test_multiple_categories(self, analytics_qa):
        assert analytics_qa["category"].nunique() >= 5
