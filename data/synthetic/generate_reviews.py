"""
Hotel Review Data Generator

Generates synthetic hotel reviews with realistic sentiment patterns,
aspect-based opinions (cleanliness, staff, food, location, value),
and temporal trends.

Output: data/synthetic/reviews.csv
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
NUM_REVIEWS = 3000

# ---------- Review templates by sentiment ----------

POSITIVE_TEMPLATES = [
    "Absolutely wonderful stay! The {aspect1} was exceptional and the {aspect2} exceeded all expectations.",
    "We had an amazing time. {aspect1_detail}. Will definitely come back!",
    "Perfect hotel for our vacation. {aspect1_detail} and {aspect2_detail}.",
    "One of the best hotels I've stayed at. {aspect1_detail}. Highly recommend!",
    "Fantastic experience from start to finish. {aspect1_detail}.",
    "Can't say enough good things about this place. {aspect1_detail} and {aspect2_detail}.",
    "Exceeded our expectations in every way. The {aspect1} was outstanding.",
    "A truly memorable stay. {aspect1_detail}. We'll be back for sure!",
    "Everything was perfect - {aspect1_detail}, {aspect2_detail}. 10/10.",
    "Best hotel experience we've had in years. {aspect1_detail}.",
]

MIXED_TEMPLATES = [
    "Overall a good stay, but {negative_detail}. On the positive side, {positive_detail}.",
    "The {pos_aspect} was great but {negative_detail}. Would still recommend.",
    "Nice hotel with some issues. {positive_detail}, however {negative_detail}.",
    "Decent stay. {positive_detail} but {negative_detail}. Room for improvement.",
    "Mixed feelings about this hotel. {positive_detail}. Unfortunately, {negative_detail}.",
    "Good but not great. {positive_detail}. The downside was {negative_detail}.",
    "The hotel has potential. {positive_detail}, yet {negative_detail}.",
    "A solid 3-star experience. {positive_detail} but {negative_detail}.",
]

NEGATIVE_TEMPLATES = [
    "Very disappointing stay. {negative_detail1} and {negative_detail2}.",
    "Would not recommend. {negative_detail1}. For the price we paid, unacceptable.",
    "Terrible experience. {negative_detail1}. {negative_detail2}. Never again.",
    "Below expectations. {negative_detail1}. Staff seemed {staff_neg}.",
    "Not worth the money. {negative_detail1} and {negative_detail2}.",
    "Worst hotel experience in a long time. {negative_detail1}.",
    "Save your money and go elsewhere. {negative_detail1}. {negative_detail2}.",
    "Hugely disappointed. {negative_detail1}. Will be filing a complaint.",
]

# Aspect-specific phrases
ASPECT_DETAILS = {
    "cleanliness": {
        "positive": [
            "The rooms were spotlessly clean",
            "Impeccable cleanliness throughout",
            "Housekeeping did an amazing job",
            "The bathroom was sparkling clean",
            "Everything was pristine and well-maintained",
        ],
        "negative": [
            "the room was not clean when we arrived",
            "found hair in the bathroom",
            "the carpets looked stained and old",
            "housekeeping missed our room twice",
            "the lobby area was dirty",
        ],
    },
    "staff": {
        "positive": [
            "The staff was incredibly friendly and helpful",
            "Reception team went above and beyond",
            "Service was impeccable from check-in to checkout",
            "The concierge gave amazing restaurant recommendations",
            "Staff remembered our names which was a nice touch",
        ],
        "negative": [
            "staff was rude at the front desk",
            "waited 20 minutes for someone to help us",
            "the reception seemed overwhelmed and disorganized",
            "staff was unresponsive to our requests",
            "no one seemed to care about guest satisfaction",
        ],
    },
    "food": {
        "positive": [
            "The breakfast buffet was outstanding with great variety",
            "Restaurant food was absolutely delicious",
            "The chef prepared an incredible dinner",
            "Room service was fast and the food was excellent",
            "Best hotel breakfast I've ever had",
        ],
        "negative": [
            "breakfast was mediocre and limited options",
            "the restaurant food was overpriced and bland",
            "room service took over an hour",
            "food quality was poor for a hotel at this price",
            "the breakfast buffet ran out of items early",
        ],
    },
    "location": {
        "positive": [
            "Perfect location, walking distance to everything",
            "The location is unbeatable - right in the center",
            "Great location near public transport",
            "Beautiful surroundings with ocean view",
            "Ideal location for both business and leisure",
        ],
        "negative": [
            "location was far from the city center",
            "noisy area with construction nearby",
            "difficult to find parking near the hotel",
            "the neighborhood felt unsafe at night",
            "very far from public transportation",
        ],
    },
    "value": {
        "positive": [
            "Excellent value for money",
            "Great price for what you get",
            "Worth every penny spent",
            "Affordable luxury at its best",
            "Best deal we found in the area",
        ],
        "negative": [
            "way overpriced for what you get",
            "not worth the price at all",
            "hidden charges everywhere",
            "much cheaper options with better quality nearby",
            "the minibar prices were outrageous",
        ],
    },
}

STAFF_NEG = ["indifferent", "unhelpful", "overwhelmed", "rude", "disinterested"]
ASPECTS = list(ASPECT_DETAILS.keys())
HOTEL_NAMES = ["Grand Resort Hotel", "City Center Hotel"]


def build_review(sentiment: str) -> dict:
    """Build a single review with aspect-level sentiments."""
    aspect_sentiments = {}

    if sentiment == "positive":
        template = np.random.choice(POSITIVE_TEMPLATES)
        rating = np.random.choice([4, 5], p=[0.3, 0.7])

        a1, a2 = np.random.choice(ASPECTS, 2, replace=False)
        aspect_sentiments = {a: np.random.choice([4, 5]) for a in ASPECTS}

        text = template.format(
            aspect1=a1,
            aspect2=a2,
            aspect1_detail=np.random.choice(ASPECT_DETAILS[a1]["positive"]),
            aspect2_detail=np.random.choice(ASPECT_DETAILS[a2]["positive"]),
        )

    elif sentiment == "mixed":
        template = np.random.choice(MIXED_TEMPLATES)
        rating = np.random.choice([3, 4], p=[0.6, 0.4])

        pos_a = np.random.choice(ASPECTS)
        neg_a = np.random.choice([a for a in ASPECTS if a != pos_a])
        aspect_sentiments = {a: np.random.choice([3, 4]) for a in ASPECTS}
        aspect_sentiments[pos_a] = np.random.choice([4, 5])
        aspect_sentiments[neg_a] = np.random.choice([1, 2])

        text = template.format(
            pos_aspect=pos_a,
            positive_detail=np.random.choice(ASPECT_DETAILS[pos_a]["positive"]),
            negative_detail=np.random.choice(ASPECT_DETAILS[neg_a]["negative"]),
        )

    else:  # negative
        template = np.random.choice(NEGATIVE_TEMPLATES)
        rating = np.random.choice([1, 2], p=[0.4, 0.6])

        n1, n2 = np.random.choice(ASPECTS, 2, replace=False)
        aspect_sentiments = {a: np.random.choice([1, 2, 3]) for a in ASPECTS}
        aspect_sentiments[n1] = np.random.choice([1, 2])
        aspect_sentiments[n2] = np.random.choice([1, 2])

        text = template.format(
            negative_detail1=np.random.choice(ASPECT_DETAILS[n1]["negative"]),
            negative_detail2=np.random.choice(ASPECT_DETAILS[n2]["negative"]),
            staff_neg=np.random.choice(STAFF_NEG),
        )

    return {"text": text, "rating": rating, "aspect_sentiments": aspect_sentiments}


def main():
    print("Generating hotel review data...")

    # Sentiment distribution: 50% positive, 25% mixed, 25% negative
    sentiments = np.random.choice(
        ["positive", "mixed", "negative"],
        size=NUM_REVIEWS,
        p=[0.50, 0.25, 0.25],
    )

    records = []
    for i, sentiment in enumerate(sentiments):
        review = build_review(sentiment)
        date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 730))

        record = {
            "review_id": f"R{i+1:04d}",
            "hotel": np.random.choice(HOTEL_NAMES, p=[0.4, 0.6]),
            "date": date.strftime("%Y-%m-%d"),
            "reviewer_country": fake.country_code(representation="alpha-2"),
            "trip_type": np.random.choice(
                ["Business", "Leisure", "Family", "Couple", "Solo"],
                p=[0.20, 0.30, 0.20, 0.20, 0.10],
            ),
            "rating": review["rating"],
            "review_text": review["text"],
            "sentiment_true": sentiment,
        }
        # Add aspect scores
        for aspect, score in review["aspect_sentiments"].items():
            record[f"aspect_{aspect}"] = score

        records.append(record)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_DIR / "reviews.csv", index=False)

    print(f"  -> {len(df)} reviews created")
    print(f"\nSentiment distribution:")
    print(df["sentiment_true"].value_counts().to_string())
    print(f"\nRating distribution:")
    print(df["rating"].value_counts().sort_index().to_string())
    print(f"\nSample review:")
    sample = df.sample(1, random_state=42).iloc[0]
    print(f"  [{sample['rating']}/5] {sample['review_text'][:120]}...")


if __name__ == "__main__":
    main()
