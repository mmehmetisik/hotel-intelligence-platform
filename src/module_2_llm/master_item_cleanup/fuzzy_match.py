"""
Master Item Cleanup — Fuzzy Matching

Uses string similarity (rapidfuzz) to match dirty product names
to standardized master items.
"""

import pandas as pd
import numpy as np
from rapidfuzz import fuzz, process
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent


def get_standard_items(df: pd.DataFrame) -> list:
    """Get unique standard item names."""
    return df["standard_name"].unique().tolist()


def fuzzy_match_single(dirty_name: str, standard_items: list, threshold: int = 70) -> tuple:
    """Match a single dirty name to the best standard item."""
    dirty_clean = dirty_name.strip().lower()

    result = process.extractOne(
        dirty_clean,
        [s.lower() for s in standard_items],
        scorer=fuzz.WRatio,
    )

    if result and result[1] >= threshold:
        idx = [s.lower() for s in standard_items].index(result[0])
        return standard_items[idx], result[1]

    return None, 0


def run_fuzzy_matching(df: pd.DataFrame, threshold: int = 70) -> pd.DataFrame:
    """Run fuzzy matching on entire dataset."""
    standard_items = get_standard_items(df)
    df = df.copy()

    matches = []
    scores = []

    for dirty_name in df["dirty_name"]:
        match, score = fuzzy_match_single(dirty_name, standard_items, threshold)
        matches.append(match)
        scores.append(score)

    df["fuzzy_match"] = matches
    df["fuzzy_score"] = scores
    df["fuzzy_correct"] = df["fuzzy_match"] == df["standard_name"]

    return df


def evaluate_fuzzy(df: pd.DataFrame) -> dict:
    """Evaluate fuzzy matching accuracy."""
    matched = df[df["fuzzy_match"].notna()]
    unmatched = df[df["fuzzy_match"].isna()]

    accuracy = df["fuzzy_correct"].mean()
    match_rate = len(matched) / len(df)

    # Accuracy only on matched items
    accuracy_on_matched = matched["fuzzy_correct"].mean() if len(matched) > 0 else 0

    logger.info(f"\nFuzzy Matching Results:")
    logger.info(f"  Overall Accuracy: {accuracy:.4f}")
    logger.info(f"  Match Rate: {match_rate:.4f} ({len(matched)}/{len(df)})")
    logger.info(f"  Accuracy on Matched: {accuracy_on_matched:.4f}")
    logger.info(f"  Avg Fuzzy Score: {df['fuzzy_score'].mean():.1f}")
    logger.info(f"  Unmatched: {len(unmatched)}")

    return {
        "method": "Fuzzy Matching",
        "accuracy": round(accuracy, 4),
        "match_rate": round(match_rate, 4),
        "accuracy_on_matched": round(accuracy_on_matched, 4),
        "avg_score": round(df["fuzzy_score"].mean(), 1),
    }


def main():
    df = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "master_items.csv")
    df = run_fuzzy_matching(df)
    results = evaluate_fuzzy(df)
    return results


if __name__ == "__main__":
    main()
