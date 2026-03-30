"""
Master Data Generator

Runs all synthetic data generators in sequence.
Usage: python data/synthetic/generate_all.py
"""

from generate_transactions import main as gen_transactions
from generate_invoices import main as gen_invoices
from generate_master_items import main as gen_master_items
from generate_reviews import main as gen_reviews
from generate_analytics_qa import main as gen_analytics_qa


def main():
    print("=" * 60)
    print("  Hotel Intelligence Platform — Data Generation")
    print("=" * 60)

    print("\n[1/5] CLTV Transaction Data")
    print("-" * 40)
    gen_transactions()

    print("\n[2/5] Invoice/POS Data")
    print("-" * 40)
    gen_invoices()

    print("\n[3/5] Master Item Data")
    print("-" * 40)
    gen_master_items()

    print("\n[4/5] Hotel Reviews")
    print("-" * 40)
    gen_reviews()

    print("\n[5/5] Analytics Q&A Pairs")
    print("-" * 40)
    gen_analytics_qa()

    print("\n" + "=" * 60)
    print("  All data generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
