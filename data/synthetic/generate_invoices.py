"""
Invoice/POS Synthetic Data Generator

Generates 5,000+ unstructured invoice line items from hotel services:
restaurant, room service, minibar, spa, parking, laundry, events.
Includes realistic typos, abbreviations, and multilingual variations.

Output: data/synthetic/invoices.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)
OUTPUT_DIR = Path(__file__).parent
NUM_INVOICES = 5500

# ---------- Item templates per category ----------

TEMPLATES = {
    "Food & Beverage - Restaurant": [
        "2x espresso + 1 croissant",
        "Breakfast buffet - {n} guests",
        "Lunch set menu: soup + main + dessert",
        "Dinner: grilled salmon with vegetables",
        "Club sandwich + french fries + {drink}",
        "Caesar salad + sparkling water",
        "Pizza Margherita + {drink}",
        "Steak medium rare with mashed potatoes",
        "Pasta carbonara + garlic bread",
        "Fish and chips + coleslaw",
        "Burger deluxe + onion rings + {drink}",
        "Thai green curry with jasmine rice",
        "Sushi platter 12 pcs",
        "Kids meal: chicken nuggets + juice",
        "Cheese platter + glass of wine",
    ],
    "Food & Beverage - Room Service": [
        "Room service: {food} + {drink} - Room {room}",
        "RS #{room}: continental breakfast",
        "Room {room} - late night snack + minibar",
        "Room service order #{room}: burger + fries + coke",
        "RS: 2x club sandwich delivered to {room}",
        "Room {room}: breakfast in bed - full english",
        "Night RS {room}: cheese toastie + tea",
    ],
    "Food & Beverage - Minibar": [
        "Minibar: {n}x beer, {m}x wine, chips",
        "Minibar consumption Room {room}",
        "MB {room}: 2 water, 1 coke, peanuts",
        "Minibar restock + consumption Rm{room}",
        "Mini bar: {n} soft drinks + snacks",
        "Minibar {room}: whisky miniature + mixer",
        "MB: {n}x juice, chocolate bar",
    ],
    "Spa & Wellness": [
        "Spa treatment - Swedish massage {duration}min",
        "Deep tissue massage {duration} minutes",
        "Couples spa package: massage + facial",
        "Aromatherapy session {duration}min",
        "Hot stone massage - {duration} min session",
        "Facial treatment - anti aging premium",
        "Spa day pass - pool + sauna + hammam",
        "Manicure + pedicure combo",
        "Body scrub + wrap treatment",
        "Yoga class - private session {duration}min",
    ],
    "Room Charges": [
        "Room upgrade: Standard to Deluxe",
        "Late checkout fee - Room {room}",
        "Early check-in surcharge",
        "Extra bed added to Room {room}",
        "Room damage charge - broken lamp",
        "Rollaway bed - {n} nights",
        "Crib rental - {n} nights",
        "Room safe deposit box",
    ],
    "Transportation": [
        "Parking {n} days - underground",
        "Airport transfer - one way",
        "Airport shuttle round trip",
        "Valet parking - {n} nights",
        "Taxi arrangement to city center",
        "Car rental arrangement - {n} days",
        "Limo service to airport",
        "Bicycle rental {n} hours",
    ],
    "Laundry & Housekeeping": [
        "Laundry service - {n} items express",
        "Dry cleaning: {n} suits",
        "Laundry: {n}x shirts, {m}x pants",
        "Express laundry same day - {n} items",
        "Ironing service - {n} pieces",
        "Housekeeping extra cleaning request",
        "Turndown service + extra towels",
    ],
    "Events & Meetings": [
        "Conference room rental - {duration}h",
        "Meeting room: half day + coffee break",
        "Projector + screen rental",
        "Business center: printing {n} pages + scanning",
        "Event space: cocktail reception {n} guests",
        "Wedding package deposit",
        "AV equipment rental full day",
        "Flipchart + markers + whiteboard",
    ],
}

DRINKS = ["coke", "sprite", "beer", "coffee", "tea", "juice", "water", "wine"]
FOODS = ["burger", "sandwich", "pasta", "salad", "soup", "pizza", "omelette"]
DURATIONS = [30, 45, 60, 90, 120]
ROOMS = list(range(101, 520))


def add_noise(text: str) -> str:
    """Add realistic typos and abbreviations."""
    r = np.random.random()
    if r < 0.08:
        # Random typo: swap two adjacent chars
        if len(text) > 4:
            idx = np.random.randint(1, len(text) - 2)
            text = text[:idx] + text[idx + 1] + text[idx] + text[idx + 2:]
    elif r < 0.15:
        # Abbreviation
        replacements = {
            "Room": "Rm", "service": "svc", "minutes": "min",
            "breakfast": "brkfst", "sandwich": "sandw",
            "Parking": "Prkg", "Laundry": "Lndry",
        }
        for full, abbr in replacements.items():
            if full in text and np.random.random() < 0.5:
                text = text.replace(full, abbr)
                break
    elif r < 0.20:
        # Lowercase everything
        text = text.lower()
    elif r < 0.24:
        # UPPERCASE everything
        text = text.upper()
    return text


def fill_template(template: str) -> str:
    """Fill placeholders in template."""
    text = template
    text = text.replace("{drink}", np.random.choice(DRINKS))
    text = text.replace("{food}", np.random.choice(FOODS))
    text = text.replace("{room}", str(np.random.choice(ROOMS)))
    text = text.replace("{duration}", str(np.random.choice(DURATIONS)))
    text = text.replace("{n}", str(np.random.randint(1, 8)))
    text = text.replace("{m}", str(np.random.randint(1, 5)))
    return text


def generate_price(category: str) -> float:
    """Generate realistic price based on category."""
    price_ranges = {
        "Food & Beverage - Restaurant": (12, 120),
        "Food & Beverage - Room Service": (18, 95),
        "Food & Beverage - Minibar": (8, 65),
        "Spa & Wellness": (45, 350),
        "Room Charges": (20, 200),
        "Transportation": (10, 250),
        "Laundry & Housekeeping": (8, 80),
        "Events & Meetings": (50, 2000),
    }
    low, high = price_ranges[category]
    return round(np.random.uniform(low, high), 2)


def main():
    print("Generating invoice data...")

    # Category distribution (weighted)
    categories = list(TEMPLATES.keys())
    weights = [0.22, 0.12, 0.10, 0.15, 0.10, 0.10, 0.08, 0.13]

    records = []
    for i in range(NUM_INVOICES):
        category = np.random.choice(categories, p=weights)
        template = np.random.choice(TEMPLATES[category])
        description = fill_template(template)
        description = add_noise(description)

        date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 730))

        records.append({
            "invoice_id": f"INV{i+1:05d}",
            "date": date.strftime("%Y-%m-%d"),
            "description": description,
            "amount": generate_price(category),
            "currency": np.random.choice(["EUR", "USD", "GBP"], p=[0.60, 0.30, 0.10]),
            "room_number": np.random.choice(ROOMS),
            "category_true": category,  # Ground truth for model evaluation
        })

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_DIR / "invoices.csv", index=False)

    print(f"  -> {len(df)} invoice records created")
    print(f"\nCategory distribution:")
    print(df["category_true"].value_counts().to_string())
    print(f"\nSample descriptions:")
    for desc in df["description"].sample(5, random_state=42).values:
        print(f"  '{desc}'")


if __name__ == "__main__":
    main()
