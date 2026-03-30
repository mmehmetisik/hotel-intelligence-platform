"""
Tests for CLTV pipeline.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))


class TestCLTVDataPrep:
    def test_load_transactions(self):
        from module_1_predictive.cltv.data_prep import load_transactions
        df = load_transactions()
        assert len(df) > 10000
        assert "customer_id" in df.columns
        assert "total_revenue" in df.columns

    def test_rfm_table(self):
        from module_1_predictive.cltv.data_prep import load_transactions, create_rfm_table
        df = load_transactions()
        rfm = create_rfm_table(df)

        assert len(rfm) > 0
        assert "recency" in rfm.columns
        assert "frequency" in rfm.columns
        assert "monetary" in rfm.columns
        # Some transactions may be after analysis_date, so recency can be negative
        assert rfm["recency"].notna().all()
        assert (rfm["frequency"] > 0).all()
        assert (rfm["monetary"] > 0).all()

    def test_rfm_scoring(self):
        from module_1_predictive.cltv.data_prep import load_transactions, create_rfm_table, score_rfm
        df = load_transactions()
        rfm = create_rfm_table(df)
        rfm = score_rfm(rfm)

        assert "R_score" in rfm.columns
        assert "F_score" in rfm.columns
        assert "M_score" in rfm.columns
        assert rfm["R_score"].between(1, 5).all()
        assert rfm["F_score"].between(1, 5).all()
        assert rfm["M_score"].between(1, 5).all()
        assert "rfm_segment" in rfm.columns
