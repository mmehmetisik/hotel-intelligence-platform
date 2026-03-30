"""
Tests for Booking Cancellation prediction pipeline.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))


class TestEDA:
    def test_load_data(self):
        from module_1_predictive.cancellation.eda import load_data
        df = load_data()
        assert len(df) > 100000
        assert "is_canceled" in df.columns
        assert df["is_canceled"].isin([0, 1]).all()

    def test_no_negative_adr(self):
        from module_1_predictive.cancellation.eda import load_data
        df = load_data()
        assert (df["adr"] >= 0).all()

    def test_no_zero_guests(self):
        from module_1_predictive.cancellation.eda import load_data
        df = load_data()
        total_guests = df["adults"] + df["children"] + df["babies"]
        assert (total_guests > 0).all()


class TestFeatureEngineering:
    @pytest.fixture
    def featured_data(self):
        from module_1_predictive.cancellation.eda import load_data
        from module_1_predictive.cancellation.features import run_feature_engineering
        df = load_data()
        df, feature_cols = run_feature_engineering(df)
        return df, feature_cols

    def test_feature_count(self, featured_data):
        df, feature_cols = featured_data
        assert len(feature_cols) >= 20

    def test_no_target_leak(self, featured_data):
        _, feature_cols = featured_data
        assert "is_canceled" not in feature_cols
        assert "reservation_status" not in feature_cols

    def test_temporal_features(self, featured_data):
        df, _ = featured_data
        assert "total_nights" in df.columns
        # season gets one-hot encoded into season_Spring, season_Summer, season_Winter
        assert any(col.startswith("season_") for col in df.columns)
        assert (df["total_nights"] >= 0).all()

    def test_customer_features(self, featured_data):
        df, _ = featured_data
        assert "total_guests" in df.columns
        assert "prev_cancel_ratio" in df.columns
        assert df["prev_cancel_ratio"].between(0, 1).all()

    def test_price_features(self, featured_data):
        df, _ = featured_data
        assert "total_cost" in df.columns
        assert "adr_per_person" in df.columns


class TestModelTraining:
    def test_data_preparation(self):
        from module_1_predictive.cancellation.eda import load_data
        from module_1_predictive.cancellation.features import run_feature_engineering
        from module_1_predictive.cancellation.train import prepare_data

        df = load_data()
        df, feature_cols = run_feature_engineering(df)
        data = prepare_data(df, feature_cols)

        assert data["X_train"].shape[0] > data["X_test"].shape[0]
        assert not data["X_train"].isnull().any().any()
        assert set(data["y_train"].unique()) == {0, 1}
