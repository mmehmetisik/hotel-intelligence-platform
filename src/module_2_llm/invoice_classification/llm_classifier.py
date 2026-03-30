"""
Invoice Classification — LLM-Based (Zero-Shot & Few-Shot)

Uses Groq API for invoice classification with:
1. Zero-shot: category from description alone
2. Few-shot: category with example demonstrations
3. Response caching to avoid redundant API calls
"""

import pandas as pd
import json
import time
import hashlib
from pathlib import Path
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent

CATEGORIES = [
    "Food & Beverage - Restaurant",
    "Food & Beverage - Room Service",
    "Food & Beverage - Minibar",
    "Spa & Wellness",
    "Room Charges",
    "Transportation",
    "Laundry & Housekeeping",
    "Events & Meetings",
]

ZERO_SHOT_PROMPT = """You are a hotel invoice classifier. Classify the following invoice description into exactly one of these categories:

Categories:
{categories}

Invoice description: "{description}"

Respond with ONLY the category name, nothing else."""

FEW_SHOT_PROMPT = """You are a hotel invoice classifier. Classify invoice descriptions into categories.

Examples:
- "2x espresso + 1 croissant" → Food & Beverage - Restaurant
- "Room service: Club sandwich + fries - Room 305" → Food & Beverage - Room Service
- "Minibar: 2 beer, 1 wine, chips" → Food & Beverage - Minibar
- "Spa treatment - Swedish massage 60min" → Spa & Wellness
- "Late checkout fee - Room 412" → Room Charges
- "Parking 3 days - underground" → Transportation
- "Laundry service - 5 items express" → Laundry & Housekeeping
- "Conference room rental - 4h" → Events & Meetings

Categories:
{categories}

Invoice description: "{description}"

Respond with ONLY the category name, nothing else."""


class LLMInvoiceClassifier:
    """LLM-based invoice classifier with caching and fallback."""

    def __init__(self, use_cache: bool = True):
        self.cache = {}
        self.use_cache = use_cache
        self.client = None
        self.api_available = False
        self._init_client()

    def _init_client(self):
        """Initialize Groq client."""
        try:
            from groq import Groq
            import os
            api_key = os.getenv("GROQ_API_KEY", "")
            if api_key:
                self.client = Groq(api_key=api_key)
                self.api_available = True
                logger.info("Groq API client initialized")
            else:
                logger.warning("GROQ_API_KEY not set. Using fallback classifier.")
        except ImportError:
            logger.warning("groq package not installed. Using fallback classifier.")

    def _cache_key(self, text: str, mode: str) -> str:
        """Generate cache key from text and mode."""
        return hashlib.md5(f"{mode}:{text}".encode()).hexdigest()

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Call Groq API with retry logic."""
        if not self.api_available:
            return None

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=50,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limit hit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"LLM call failed: {e}")
                    return None
        return None

    def _fallback_classify(self, description: str) -> str:
        """Simple keyword fallback when LLM is unavailable."""
        desc_lower = description.lower()

        keyword_map = {
            "Food & Beverage - Minibar": ["minibar", "mini bar", "mb "],
            "Food & Beverage - Room Service": ["room service", "rs ", "rs:", "delivered to"],
            "Spa & Wellness": ["spa", "massage", "facial", "sauna", "yoga", "manicure"],
            "Transportation": ["parking", "airport", "transfer", "taxi", "shuttle", "bicycle"],
            "Laundry & Housekeeping": ["laundry", "dry clean", "ironing", "housekeeping"],
            "Events & Meetings": ["conference", "meeting", "projector", "event", "wedding"],
            "Room Charges": ["upgrade", "checkout", "check-in", "extra bed", "crib", "damage"],
        }

        for category, keywords in keyword_map.items():
            if any(kw in desc_lower for kw in keywords):
                return category

        return "Food & Beverage - Restaurant"  # Default for food items

    def classify_zero_shot(self, description: str) -> str:
        """Classify using zero-shot prompting."""
        cache_key = self._cache_key(description, "zero_shot")

        if self.use_cache and cache_key in self.cache:
            return self.cache[cache_key]

        prompt = ZERO_SHOT_PROMPT.format(
            categories="\n".join(f"- {c}" for c in CATEGORIES),
            description=description,
        )

        result = self._call_llm(prompt)
        if result is None:
            result = self._fallback_classify(description)

        # Validate result is a known category
        if result not in CATEGORIES:
            # Try fuzzy match
            result_lower = result.lower()
            for cat in CATEGORIES:
                if cat.lower() in result_lower or result_lower in cat.lower():
                    result = cat
                    break
            else:
                result = self._fallback_classify(description)

        if self.use_cache:
            self.cache[cache_key] = result

        return result

    def classify_few_shot(self, description: str) -> str:
        """Classify using few-shot prompting."""
        cache_key = self._cache_key(description, "few_shot")

        if self.use_cache and cache_key in self.cache:
            return self.cache[cache_key]

        prompt = FEW_SHOT_PROMPT.format(
            categories="\n".join(f"- {c}" for c in CATEGORIES),
            description=description,
        )

        result = self._call_llm(prompt)
        if result is None:
            result = self._fallback_classify(description)

        if result not in CATEGORIES:
            result_lower = result.lower()
            for cat in CATEGORIES:
                if cat.lower() in result_lower or result_lower in cat.lower():
                    result = cat
                    break
            else:
                result = self._fallback_classify(description)

        if self.use_cache:
            self.cache[cache_key] = result

        return result

    def classify_batch(self, descriptions: list, mode: str = "few_shot") -> list:
        """Classify a batch of descriptions."""
        classify_fn = self.classify_few_shot if mode == "few_shot" else self.classify_zero_shot

        results = []
        for i, desc in enumerate(descriptions):
            result = classify_fn(desc)
            results.append(result)

            if (i + 1) % 100 == 0:
                logger.info(f"  Classified {i+1}/{len(descriptions)}")

        return results


def evaluate_llm(df: pd.DataFrame, mode: str = "few_shot") -> dict:
    """Evaluate LLM classification."""
    from sklearn.metrics import classification_report, accuracy_score

    classifier = LLMInvoiceClassifier()

    logger.info(f"\nRunning LLM classification ({mode})...")
    predictions = classifier.classify_batch(df["description"].tolist(), mode=mode)
    df = df.copy()
    df["predicted_category"] = predictions

    y_true = df["category_true"]
    y_pred = df["predicted_category"]

    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    logger.info(f"\nLLM {mode} Classification Results:")
    logger.info(f"  Overall Accuracy: {accuracy:.4f}")
    logger.info(f"  API Available: {classifier.api_available}")
    logger.info(f"\n{classification_report(y_true, y_pred, zero_division=0)}")

    return {
        "method": f"LLM ({mode})",
        "accuracy": round(accuracy, 4),
        "report": report,
        "api_used": classifier.api_available,
    }


def main():
    df = pd.read_csv(ROOT_DIR / "data" / "synthetic" / "invoices.csv")

    # Run on a sample for speed (full dataset with API would take too long)
    sample = df.sample(500, random_state=42)

    results_zero = evaluate_llm(sample, mode="zero_shot")
    results_few = evaluate_llm(sample, mode="few_shot")

    return {"zero_shot": results_zero, "few_shot": results_few}


if __name__ == "__main__":
    main()
