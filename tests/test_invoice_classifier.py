"""
Tests for Invoice Classification and Master Item Cleanup.
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))


class TestRuleBasedClassifier:
    def test_classify_restaurant(self):
        from module_2_llm.invoice_classification.rule_based import classify_rule_based
        assert classify_rule_based("2x espresso + 1 croissant") == "Food & Beverage - Restaurant"

    def test_classify_minibar(self):
        from module_2_llm.invoice_classification.rule_based import classify_rule_based
        assert classify_rule_based("Minibar: 2 beer, 1 wine") == "Food & Beverage - Minibar"

    def test_classify_spa(self):
        from module_2_llm.invoice_classification.rule_based import classify_rule_based
        assert classify_rule_based("Swedish massage 60min") == "Spa & Wellness"

    def test_classify_parking(self):
        from module_2_llm.invoice_classification.rule_based import classify_rule_based
        assert classify_rule_based("Parking 3 days underground") == "Transportation"

    def test_classify_laundry(self):
        from module_2_llm.invoice_classification.rule_based import classify_rule_based
        assert classify_rule_based("Laundry service 5 items") == "Laundry & Housekeeping"

    def test_classify_room_service(self):
        from module_2_llm.invoice_classification.rule_based import classify_rule_based
        assert classify_rule_based("Room service: burger + fries Room 305") == "Food & Beverage - Room Service"

    def test_full_dataset_accuracy(self):
        from module_2_llm.invoice_classification.rule_based import main
        results = main()
        assert results["accuracy"] > 0.70, "Rule-based should achieve > 70% accuracy"


class TestFuzzyMatching:
    def test_exact_match(self):
        from module_2_llm.master_item_cleanup.fuzzy_match import fuzzy_match_single
        standards = ["Coca-Cola 330ml", "Pepsi 500ml"]
        match, score = fuzzy_match_single("coca cola 330ml", standards)
        assert match == "Coca-Cola 330ml"
        assert score > 70

    def test_abbreviation_match(self):
        from module_2_llm.master_item_cleanup.fuzzy_match import fuzzy_match_single
        standards = ["Spaghetti Bolognese", "Caesar Salad"]
        # "spag bol" is a very short abbreviation, lower threshold needed
        match, score = fuzzy_match_single("spag bol", standards, threshold=45)
        assert match == "Spaghetti Bolognese"

    def test_full_dataset_accuracy(self):
        from module_2_llm.master_item_cleanup.fuzzy_match import main
        results = main()
        assert results["accuracy"] > 0.50, "Fuzzy matching should achieve > 50% accuracy"


class TestReviewAnalysis:
    def test_sentiment_keywords(self):
        from module_2_llm.review_analysis.sentiment import SentimentAnalyzer
        analyzer = SentimentAnalyzer()

        pos = analyzer.rule_based_sentiment("Absolutely wonderful amazing stay!")
        assert pos["sentiment"] == "positive"

        neg = analyzer.rule_based_sentiment("Terrible awful horrible experience")
        assert neg["sentiment"] == "negative"

    def test_aspect_extraction(self):
        from module_2_llm.review_analysis.sentiment import SentimentAnalyzer
        analyzer = SentimentAnalyzer()

        aspects = analyzer.extract_aspects("The staff was friendly and the food was delicious")
        assert aspects["staff"] is True
        assert aspects["food"] is True
