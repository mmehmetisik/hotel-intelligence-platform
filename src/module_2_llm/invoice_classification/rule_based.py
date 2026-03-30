"""
Invoice Classification — Rule-Based Baseline

Classifies hotel invoice descriptions using regex and keyword matching.
Serves as a baseline to compare against LLM approaches.
"""

import re
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent

# Category rules: list of (pattern, category) tuples — first match wins
RULES = [
    # Food & Beverage - Minibar
    (r"(?i)\b(minibar|mini.?bar|MB\b)", "Food & Beverage - Minibar"),

    # Food & Beverage - Room Service
    (r"(?i)\b(room.?service|RS\b|RS\s*#|RS:)", "Food & Beverage - Room Service"),
    (r"(?i)room\s+\d{3}.*(?:breakfast|snack|sandwich|burger|order)", "Food & Beverage - Room Service"),
    (r"(?i)(?:delivered|deliver)\s+to\s+\d{3}", "Food & Beverage - Room Service"),

    # Spa & Wellness
    (r"(?i)\b(spa|massage|facial|manicure|pedicure|sauna|hammam|yoga|body.?scrub|aromatherapy|hot.?stone|wellness|treatment)", "Spa & Wellness"),

    # Transportation
    (r"(?i)\b(parking|prkg|valet|airport|transfer|shuttle|taxi|limo|car.?rental|bicycle)", "Transportation"),

    # Laundry & Housekeeping
    (r"(?i)\b(laundry|lndry|dry.?clean|ironing|housekeeping|turndown|towel)", "Laundry & Housekeeping"),

    # Events & Meetings
    (r"(?i)\b(conference|meeting|projector|business.?center|event|wedding|AV\s+equip|flipchart|cocktail.?reception)", "Events & Meetings"),

    # Room Charges
    (r"(?i)\b(room.?upgrade|late.?checkout|early.?check|extra.?bed|room.?damage|rollaway|crib|safe.?deposit)", "Room Charges"),

    # Food & Beverage - Restaurant (catch-all for food)
    (r"(?i)\b(breakfast|lunch|dinner|buffet|restaurant|pizza|pasta|burger|salad|sandwich|steak|salmon|sushi|curry|soup|dessert|croissant|espresso|cappuccino|latte|coffee|tea|beer|wine|coke|sprite|juice|fries|chicken|fish|cheese)", "Food & Beverage - Restaurant"),
]


def classify_rule_based(description: str) -> str:
    """Classify a single invoice description using rules."""
    for pattern, category in RULES:
        if re.search(pattern, description):
            return category
    return "Other"


def run_rule_based_classification(df: pd.DataFrame) -> pd.DataFrame:
    """Run rule-based classification on entire dataset."""
    df = df.copy()
    df["predicted_category"] = df["description"].apply(classify_rule_based)
    return df


def evaluate(df: pd.DataFrame) -> dict:
    """Evaluate rule-based classification accuracy."""
    from sklearn.metrics import classification_report, accuracy_score

    y_true = df["category_true"]
    y_pred = df["predicted_category"]

    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    logger.info(f"\nRule-Based Classification Results:")
    logger.info(f"  Overall Accuracy: {accuracy:.4f}")
    logger.info(f"\n{classification_report(y_true, y_pred, zero_division=0)}")

    return {
        "method": "Rule-Based",
        "accuracy": round(accuracy, 4),
        "report": report,
    }


def main():
    df = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "invoices.csv")
    df = run_rule_based_classification(df)
    results = evaluate(df)
    return results


if __name__ == "__main__":
    main()
