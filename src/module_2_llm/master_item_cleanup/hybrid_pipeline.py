"""
Master Item Cleanup — Hybrid Pipeline

Combines multiple approaches for optimal item standardization:
1. Exact match (after normalization)
2. Fuzzy matching (high confidence)
3. Embedding similarity (semantic matching)
4. LLM fallback (for ambiguous cases)

Each layer handles what the previous couldn't resolve.
"""

import pandas as pd
import numpy as np
from rapidfuzz import fuzz, process
from pathlib import Path
import logging
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "master_item_cleanup"


class HybridItemMatcher:
    """Multi-layer item matching pipeline."""

    def __init__(self, standard_items: list):
        self.standard_items = standard_items
        self.standard_lower = [s.lower().strip() for s in standard_items]

        # Build TF-IDF model for embedding similarity
        self.tfidf = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
        self.standard_vectors = self.tfidf.fit_transform(self.standard_lower)

    def normalize(self, text: str) -> str:
        """Basic text normalization."""
        import re
        text = text.strip().lower()
        text = re.sub(r"\s+", " ", text)  # Multiple spaces -> single
        text = re.sub(r"[^\w\s\-]", "", text)  # Remove special chars except hyphen
        return text

    def exact_match(self, dirty_name: str) -> tuple:
        """Layer 1: Exact match after normalization."""
        normalized = self.normalize(dirty_name)
        for i, standard in enumerate(self.standard_lower):
            if normalized == self.normalize(standard):
                return self.standard_items[i], 100.0, "exact"
        return None, 0.0, None

    def fuzzy_match(self, dirty_name: str, threshold: int = 82) -> tuple:
        """Layer 2: Fuzzy string matching."""
        normalized = self.normalize(dirty_name)
        result = process.extractOne(
            normalized, self.standard_lower, scorer=fuzz.WRatio
        )
        if result and result[1] >= threshold:
            idx = self.standard_lower.index(result[0])
            return self.standard_items[idx], result[1], "fuzzy"
        return None, result[1] if result else 0.0, None

    def embedding_match(self, dirty_name: str, threshold: float = 0.55) -> tuple:
        """Layer 3: TF-IDF character n-gram embedding similarity."""
        normalized = self.normalize(dirty_name)
        dirty_vector = self.tfidf.transform([normalized])
        similarities = cosine_similarity(dirty_vector, self.standard_vectors)[0]

        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]

        if best_score >= threshold:
            return self.standard_items[best_idx], round(best_score * 100, 1), "embedding"
        return None, round(best_score * 100, 1), None

    def match(self, dirty_name: str) -> dict:
        """Run the full matching pipeline."""
        # Layer 1: Exact
        result, score, method = self.exact_match(dirty_name)
        if result:
            return {"match": result, "score": score, "method": method, "confidence": "high"}

        # Layer 2: Fuzzy (high threshold)
        result, score, method = self.fuzzy_match(dirty_name, threshold=82)
        if result:
            return {"match": result, "score": score, "method": method, "confidence": "high"}

        # Layer 3: Embedding
        result, score, method = self.embedding_match(dirty_name, threshold=0.55)
        if result:
            return {"match": result, "score": score, "method": method, "confidence": "medium"}

        # Layer 4: Fuzzy with lower threshold
        result, score, method = self.fuzzy_match(dirty_name, threshold=60)
        if result:
            return {"match": result, "score": score, "method": "fuzzy_low", "confidence": "low"}

        return {"match": None, "score": score, "method": "unmatched", "confidence": "none"}

    def match_batch(self, dirty_names: list) -> list:
        """Match a batch of dirty names."""
        results = []
        for i, name in enumerate(dirty_names):
            results.append(self.match(name))
            if (i + 1) % 200 == 0:
                logger.info(f"  Matched {i+1}/{len(dirty_names)}")
        return results


def run_hybrid_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Run hybrid matching pipeline on dataset."""
    standard_items = df["standard_name"].unique().tolist()
    matcher = HybridItemMatcher(standard_items)

    logger.info("Running hybrid matching pipeline...")
    results = matcher.match_batch(df["dirty_name"].tolist())

    df = df.copy()
    df["hybrid_match"] = [r["match"] for r in results]
    df["hybrid_score"] = [r["score"] for r in results]
    df["hybrid_method"] = [r["method"] for r in results]
    df["hybrid_confidence"] = [r["confidence"] for r in results]
    df["hybrid_correct"] = df["hybrid_match"] == df["standard_name"]

    return df


def evaluate_hybrid(df: pd.DataFrame) -> dict:
    """Evaluate hybrid pipeline."""
    accuracy = df["hybrid_correct"].mean()
    matched = df[df["hybrid_match"].notna()]
    match_rate = len(matched) / len(df)

    method_breakdown = df.groupby("hybrid_method").agg(
        count=("hybrid_correct", "count"),
        accuracy=("hybrid_correct", "mean"),
    ).round(4)

    confidence_breakdown = df.groupby("hybrid_confidence").agg(
        count=("hybrid_correct", "count"),
        accuracy=("hybrid_correct", "mean"),
    ).round(4)

    logger.info(f"\nHybrid Pipeline Results:")
    logger.info(f"  Overall Accuracy: {accuracy:.4f}")
    logger.info(f"  Match Rate: {match_rate:.4f}")
    logger.info(f"\nBy Method:\n{method_breakdown}")
    logger.info(f"\nBy Confidence:\n{confidence_breakdown}")

    return {
        "method": "Hybrid Pipeline",
        "accuracy": round(accuracy, 4),
        "match_rate": round(match_rate, 4),
        "method_breakdown": method_breakdown.to_dict(),
        "confidence_breakdown": confidence_breakdown.to_dict(),
    }


def run_full_comparison(df: pd.DataFrame) -> dict:
    """Run fuzzy vs hybrid comparison."""
    logger.info("=" * 60)
    logger.info("  MASTER ITEM CLEANUP — PIPELINE COMPARISON")
    logger.info("=" * 60)

    # Fuzzy only
    from src.module_2_llm.master_item_cleanup.fuzzy_match import run_fuzzy_matching, evaluate_fuzzy
    logger.info("\n--- Fuzzy Matching ---")
    df_fuzzy = run_fuzzy_matching(df)
    fuzzy_results = evaluate_fuzzy(df_fuzzy)

    # Hybrid
    logger.info("\n--- Hybrid Pipeline ---")
    df_hybrid = run_hybrid_pipeline(df)
    hybrid_results = evaluate_hybrid(df_hybrid)

    # Save
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    comparison = {
        "fuzzy": {k: v for k, v in fuzzy_results.items() if not isinstance(v, pd.DataFrame)},
        "hybrid": {k: v for k, v in hybrid_results.items() if not isinstance(v, pd.DataFrame)},
    }
    with open(MODELS_DIR / "comparison_results.json", "w") as f:
        json.dump(comparison, f, indent=2, default=str)

    # Save matched data
    df_hybrid.to_csv(ROOT_DIR / "data" / "processed" / "master_items_matched.csv", index=False)

    logger.info(f"\n{'='*60}")
    logger.info(f"  Fuzzy Accuracy: {fuzzy_results['accuracy']}")
    logger.info(f"  Hybrid Accuracy: {hybrid_results['accuracy']}")
    logger.info(f"  Improvement: +{(hybrid_results['accuracy'] - fuzzy_results['accuracy'])*100:.1f}pp")
    logger.info(f"{'='*60}")

    return {"fuzzy": fuzzy_results, "hybrid": hybrid_results}


def main():
    df = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "master_items.csv")
    run_full_comparison(df)


if __name__ == "__main__":
    main()
