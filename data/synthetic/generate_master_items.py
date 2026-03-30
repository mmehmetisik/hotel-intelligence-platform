"""
Master Item Dirty Data Generator

Generates 1,000+ dirty, inconsistent product names that need
standardization. Simulates real-world POS data with typos,
abbreviations, different languages, and format variations.

Output: data/synthetic/master_items.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
OUTPUT_DIR = Path(__file__).parent

# ---------- Standard items and their dirty variations ----------

MASTER_ITEMS = {
    # Beverages
    "Coca-Cola 330ml": [
        "Coke 330ml", "coca cola", "CC can", "Coca Cola 33cl",
        "coke", "COCA-COLA", "Coka Cola", "coca-cola 330",
        "Diet Coke 330ml", "coke can", "Coca Cola Can",
    ],
    "Pepsi 500ml": [
        "Pepsi Cola 500", "peps 500ml", "PEPSI", "pepsi cola",
        "Pepsi 50cl", "pepsi 500", "Pepsii 500ml",
    ],
    "Sprite 330ml": [
        "sprite", "Sprite can", "SPRITE 330", "Sprit 330ml",
        "sprite 33cl", "Srpite",
    ],
    "Still Water 500ml": [
        "water 500ml", "Water", "still water", "WATER 500",
        "Evian 500ml", "San Pellegrino 500ml", "aqua 500",
        "mineral water", "H2O 500ml",
    ],
    "Sparkling Water 500ml": [
        "sparkling water", "Sparkling 500ml", "soda water",
        "sprkl water", "fizzy water 500", "SPARKLING",
    ],
    "Fresh Orange Juice": [
        "OJ", "orange juice", "fresh OJ", "Orange J.",
        "Orng juice", "ORANGE JUICE", "frsh orange juice",
    ],
    "Espresso": [
        "espresso", "Expresso", "ESPRESSO", "esprso",
        "single espresso", "1x espresso", "cafe espresso",
    ],
    "Cappuccino": [
        "cappuccino", "Cappucino", "CAPPUCCINO", "capuccino",
        "cap.", "cappucc.", "cafe cappuccino",
    ],
    "Latte": [
        "latte", "Cafe Latte", "LATTE", "caffe latte",
        "cafe latte", "Lattee",
    ],
    "House Red Wine (Glass)": [
        "red wine glass", "House Red", "wine red",
        "glass of red wine", "RED WINE", "vino rosso",
        "red wine", "hse red wine",
    ],
    "House White Wine (Glass)": [
        "white wine glass", "House White", "wine white",
        "glass of white wine", "WHITE WINE", "vino bianco",
        "white wine", "hse white wine",
    ],
    "Local Beer Draft 500ml": [
        "draft beer", "beer 500ml", "Beer draft", "BEER",
        "local beer", "bier 500", "draught beer", "drft beer",
    ],
    # Food
    "Club Sandwich": [
        "Club Sandw.", "club sandwich", "CLUB SANDWICH",
        "Club SW", "clb sandwich", "club sandwhich",
    ],
    "Caesar Salad": [
        "caesar salad", "Ceasar Salad", "CAESAR SALAD",
        "cesar salad", "Caeser Salad", "caesar sld",
    ],
    "Margherita Pizza": [
        "Pizza Margherita", "margherita", "MARGHERITA PIZZA",
        "pizza marg.", "Margarita Pizza", "Margherita Pzza",
    ],
    "Spaghetti Bolognese": [
        "Spagetti Bolognese", "spag bol", "SPAGHETTI BOL",
        "spaghetti bolognaise", "Spag. Bolognese", "bolognese pasta",
    ],
    "French Fries": [
        "fries", "French Fries", "FRIES", "french fries",
        "chips", "pommes frites", "FF", "frech fries",
    ],
    "Grilled Chicken Breast": [
        "grilled chicken", "Chicken Breast", "GRILLED CHICKEN",
        "grld chicken", "chicken brst grilled", "pollo alla griglia",
    ],
    "Beef Burger": [
        "burger", "Beef Burger", "BURGER", "hamburger",
        "beef brgr", "cheese burger", "beef hamburger",
    ],
    "Chocolate Cake": [
        "choc cake", "Chocolate Cake", "CHOC CAKE",
        "chocolate ck", "choco cake", "Schoko Kuchen",
    ],
    # Spa
    "Swedish Massage 60min": [
        "swedish massage", "Swedish 60min", "SWEDISH MASSAGE",
        "swedish mass. 60", "Swdsh Massage 1hr", "massage swedish 60",
    ],
    "Deep Tissue Massage 60min": [
        "deep tissue 60", "Deep Tissue", "DEEP TISSUE MASSAGE",
        "deep tissue mass.", "DT massage 60min",
    ],
    "Facial Treatment": [
        "facial", "Facial Treatment", "FACIAL", "face treatment",
        "facial treatmnt", "skin facial",
    ],
    # Services
    "Underground Parking (per day)": [
        "parking", "Parking 1 day", "PARKING", "underground parking",
        "prkg daily", "car park 1d", "Parking p/day",
    ],
    "Airport Transfer One Way": [
        "airport transfer", "Transfer Airport", "AIRPORT TRANSFER",
        "airport trnsf", "airprt transfer 1way", "transfer to airport",
    ],
    "Laundry Service (per item)": [
        "laundry", "Laundry 1 item", "LAUNDRY", "laundry svc",
        "lndry service", "wash + iron", "laundry per piece",
    ],
    "Dry Cleaning (per item)": [
        "dry cleaning", "Dry Clean", "DRY CLEANING",
        "dry cln", "dry cleaning 1pc", "chemical cleaning",
    ],
}


def generate_dirty_records(n: int = 1200) -> pd.DataFrame:
    """Generate dirty item records from master item variations."""
    records = []
    standard_items = list(MASTER_ITEMS.keys())

    for i in range(n):
        standard = np.random.choice(standard_items)
        variations = MASTER_ITEMS[standard]
        dirty_name = np.random.choice(variations)

        # Additional noise
        r = np.random.random()
        if r < 0.05:
            dirty_name = dirty_name + " "  # trailing space
        elif r < 0.10:
            dirty_name = " " + dirty_name  # leading space
        elif r < 0.14:
            dirty_name = dirty_name.replace(" ", "  ")  # double space

        # Determine category
        if standard in ["Coca-Cola 330ml", "Pepsi 500ml", "Sprite 330ml",
                         "Still Water 500ml", "Sparkling Water 500ml",
                         "Fresh Orange Juice", "Espresso", "Cappuccino",
                         "Latte", "House Red Wine (Glass)",
                         "House White Wine (Glass)", "Local Beer Draft 500ml"]:
            category = "Beverage"
        elif standard in ["Club Sandwich", "Caesar Salad", "Margherita Pizza",
                           "Spaghetti Bolognese", "French Fries",
                           "Grilled Chicken Breast", "Beef Burger",
                           "Chocolate Cake"]:
            category = "Food"
        elif standard in ["Swedish Massage 60min", "Deep Tissue Massage 60min",
                           "Facial Treatment"]:
            category = "Spa"
        else:
            category = "Service"

        records.append({
            "item_id": f"ITM{i+1:04d}",
            "dirty_name": dirty_name,
            "standard_name": standard,  # Ground truth
            "category": category,
            "unit_price": round(np.random.uniform(2, 150), 2),
            "source_system": np.random.choice(
                ["POS_Restaurant", "POS_Bar", "POS_Spa", "PMS", "Manual"],
                p=[0.30, 0.20, 0.15, 0.25, 0.10],
            ),
        })

    return pd.DataFrame(records)


def main():
    print("Generating master item dirty data...")
    df = generate_dirty_records(1200)
    df.to_csv(OUTPUT_DIR / "master_items.csv", index=False)

    print(f"  -> {len(df)} dirty item records created")
    print(f"  -> {df['standard_name'].nunique()} unique standard items")
    print(f"\nCategory distribution:")
    print(df["category"].value_counts().to_string())
    print(f"\nSample dirty vs standard:")
    sample = df.sample(5, random_state=42)
    for _, row in sample.iterrows():
        print(f"  '{row['dirty_name']}' -> '{row['standard_name']}'")


if __name__ == "__main__":
    main()
