"""
Analytics Q&A Pairs Generator

Generates 120+ question-answer pairs for training and testing the
Conversational AI module. Covers booking analytics, revenue,
customer segments, occupancy, and operational KPIs.

Output: data/synthetic/analytics_qa.csv
"""

import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

QA_PAIRS = [
    # --- Booking & Cancellation ---
    {
        "question": "What was the cancellation rate last month?",
        "intent": "cancellation_rate",
        "sql_template": "SELECT COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as rate FROM bookings WHERE strftime('%Y-%m', arrival_date) = '{last_month}'",
        "expected_viz": "metric",
        "category": "cancellation",
    },
    {
        "question": "Show me the cancellation trend over the last 12 months",
        "intent": "cancellation_trend",
        "sql_template": "SELECT strftime('%Y-%m', arrival_date) as month, COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as cancel_rate FROM bookings GROUP BY month ORDER BY month",
        "expected_viz": "line_chart",
        "category": "cancellation",
    },
    {
        "question": "Which customer segment has the highest cancellation rate?",
        "intent": "cancellation_by_segment",
        "sql_template": "SELECT customer_type, COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as cancel_rate FROM bookings GROUP BY customer_type ORDER BY cancel_rate DESC",
        "expected_viz": "bar_chart",
        "category": "cancellation",
    },
    {
        "question": "How does lead time affect cancellations?",
        "intent": "cancellation_by_leadtime",
        "sql_template": "SELECT CASE WHEN lead_time<30 THEN '0-30' WHEN lead_time<90 THEN '30-90' WHEN lead_time<180 THEN '90-180' ELSE '180+' END as lead_bucket, COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as cancel_rate FROM bookings GROUP BY lead_bucket",
        "expected_viz": "bar_chart",
        "category": "cancellation",
    },
    {
        "question": "What is the cancellation rate by deposit type?",
        "intent": "cancellation_by_deposit",
        "sql_template": "SELECT deposit_type, COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as cancel_rate FROM bookings GROUP BY deposit_type",
        "expected_viz": "bar_chart",
        "category": "cancellation",
    },
    {
        "question": "How many bookings were cancelled this quarter?",
        "intent": "cancellation_count",
        "sql_template": "SELECT COUNT(*) FROM bookings WHERE is_canceled=1 AND strftime('%Y', arrival_date)='{year}' AND ((strftime('%m', arrival_date)-1)/3 + 1) = {quarter}",
        "expected_viz": "metric",
        "category": "cancellation",
    },
    {
        "question": "Compare cancellation rates between resort and city hotels",
        "intent": "cancellation_by_hotel",
        "sql_template": "SELECT hotel, COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as cancel_rate FROM bookings GROUP BY hotel",
        "expected_viz": "bar_chart",
        "category": "cancellation",
    },
    # --- Revenue ---
    {
        "question": "What is the total revenue this year?",
        "intent": "total_revenue",
        "sql_template": "SELECT SUM(total_revenue) FROM transactions WHERE strftime('%Y', transaction_date)='{year}'",
        "expected_viz": "metric",
        "category": "revenue",
    },
    {
        "question": "Show me monthly revenue trend",
        "intent": "revenue_trend",
        "sql_template": "SELECT strftime('%Y-%m', transaction_date) as month, SUM(total_revenue) as revenue FROM transactions GROUP BY month ORDER BY month",
        "expected_viz": "line_chart",
        "category": "revenue",
    },
    {
        "question": "What is the average daily rate by room type?",
        "intent": "adr_by_room",
        "sql_template": "SELECT room_type, AVG(daily_rate) as avg_rate FROM transactions GROUP BY room_type ORDER BY avg_rate DESC",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
    {
        "question": "Show me top 10 customers by total revenue",
        "intent": "top_customers_revenue",
        "sql_template": "SELECT customer_id, SUM(total_revenue) as total, COUNT(*) as visits FROM transactions GROUP BY customer_id ORDER BY total DESC LIMIT 10",
        "expected_viz": "table",
        "category": "revenue",
    },
    {
        "question": "What is the revenue breakdown by booking channel?",
        "intent": "revenue_by_channel",
        "sql_template": "SELECT booking_channel, SUM(total_revenue) as revenue FROM transactions GROUP BY booking_channel ORDER BY revenue DESC",
        "expected_viz": "pie_chart",
        "category": "revenue",
    },
    {
        "question": "Compare Q1 vs Q2 revenue",
        "intent": "revenue_quarterly_compare",
        "sql_template": "SELECT CASE WHEN strftime('%m', transaction_date) IN ('01','02','03') THEN 'Q1' WHEN strftime('%m', transaction_date) IN ('04','05','06') THEN 'Q2' END as quarter, SUM(total_revenue) as revenue FROM transactions WHERE quarter IS NOT NULL GROUP BY quarter",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
    {
        "question": "What is the average revenue per booking?",
        "intent": "avg_revenue_per_booking",
        "sql_template": "SELECT AVG(total_revenue) FROM transactions",
        "expected_viz": "metric",
        "category": "revenue",
    },
    {
        "question": "Revenue by hotel type for the last 6 months",
        "intent": "revenue_by_hotel_type",
        "sql_template": "SELECT hotel_type, SUM(total_revenue) as revenue FROM transactions WHERE transaction_date >= date('now', '-6 months') GROUP BY hotel_type",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
    # --- Customer & Segments ---
    {
        "question": "How many customers do we have in each segment?",
        "intent": "segment_distribution",
        "sql_template": "SELECT segment, COUNT(*) as count FROM customer_segments GROUP BY segment ORDER BY count DESC",
        "expected_viz": "bar_chart",
        "category": "customer",
    },
    {
        "question": "Which customer segment has the highest churn risk?",
        "intent": "churn_risk_segment",
        "sql_template": "SELECT segment, COUNT(*) as count, AVG(recency) as avg_recency FROM customer_segments WHERE segment IN ('at_risk', 'lost') GROUP BY segment",
        "expected_viz": "table",
        "category": "customer",
    },
    {
        "question": "What is the average CLTV by customer segment?",
        "intent": "cltv_by_segment",
        "sql_template": "SELECT segment, AVG(cltv) as avg_cltv FROM customer_segments GROUP BY segment ORDER BY avg_cltv DESC",
        "expected_viz": "bar_chart",
        "category": "customer",
    },
    {
        "question": "Show me the RFM distribution of our customers",
        "intent": "rfm_distribution",
        "sql_template": "SELECT rfm_score, COUNT(*) as count FROM customer_segments GROUP BY rfm_score ORDER BY rfm_score",
        "expected_viz": "histogram",
        "category": "customer",
    },
    {
        "question": "How many repeat customers do we have?",
        "intent": "repeat_customers",
        "sql_template": "SELECT COUNT(DISTINCT customer_id) FROM transactions GROUP BY customer_id HAVING COUNT(*) > 1",
        "expected_viz": "metric",
        "category": "customer",
    },
    {
        "question": "What percentage of revenue comes from top 20% customers?",
        "intent": "pareto_revenue",
        "sql_template": "SELECT customer_id, SUM(total_revenue) as total FROM transactions GROUP BY customer_id ORDER BY total DESC",
        "expected_viz": "metric",
        "category": "customer",
    },
    {
        "question": "Customer distribution by country - top 10",
        "intent": "customers_by_country",
        "sql_template": "SELECT country, COUNT(*) as count FROM customers GROUP BY country ORDER BY count DESC LIMIT 10",
        "expected_viz": "bar_chart",
        "category": "customer",
    },
    {
        "question": "Show champion customers with their total spend",
        "intent": "champion_customers",
        "sql_template": "SELECT c.customer_id, SUM(t.total_revenue) as total_spend, COUNT(*) as visits FROM customer_segments c JOIN transactions t ON c.customer_id=t.customer_id WHERE c.segment='champion' GROUP BY c.customer_id ORDER BY total_spend DESC LIMIT 20",
        "expected_viz": "table",
        "category": "customer",
    },
    # --- Occupancy ---
    {
        "question": "What is the current occupancy rate?",
        "intent": "occupancy_current",
        "sql_template": "SELECT occupied_rooms*100.0/total_rooms as occupancy_rate FROM daily_metrics ORDER BY date DESC LIMIT 1",
        "expected_viz": "metric",
        "category": "occupancy",
    },
    {
        "question": "Compare weekend vs weekday occupancy",
        "intent": "occupancy_weekend_weekday",
        "sql_template": "SELECT CASE WHEN strftime('%w', date) IN ('0','6') THEN 'Weekend' ELSE 'Weekday' END as day_type, AVG(occupancy_rate) as avg_occupancy FROM daily_metrics GROUP BY day_type",
        "expected_viz": "bar_chart",
        "category": "occupancy",
    },
    {
        "question": "Show occupancy trend for the last 3 months",
        "intent": "occupancy_trend",
        "sql_template": "SELECT date, occupancy_rate FROM daily_metrics WHERE date >= date('now', '-3 months') ORDER BY date",
        "expected_viz": "line_chart",
        "category": "occupancy",
    },
    {
        "question": "Which month had the highest occupancy last year?",
        "intent": "occupancy_best_month",
        "sql_template": "SELECT strftime('%m', date) as month, AVG(occupancy_rate) as avg_occ FROM daily_metrics WHERE strftime('%Y', date)='{last_year}' GROUP BY month ORDER BY avg_occ DESC LIMIT 1",
        "expected_viz": "metric",
        "category": "occupancy",
    },
    {
        "question": "Compare occupancy between resort and city hotels",
        "intent": "occupancy_by_hotel",
        "sql_template": "SELECT hotel_type, AVG(occupancy_rate) as avg_occupancy FROM daily_metrics GROUP BY hotel_type",
        "expected_viz": "bar_chart",
        "category": "occupancy",
    },
    # --- Operations ---
    {
        "question": "What are the most common special requests?",
        "intent": "special_requests",
        "sql_template": "SELECT special_request, COUNT(*) as count FROM booking_requests GROUP BY special_request ORDER BY count DESC LIMIT 10",
        "expected_viz": "bar_chart",
        "category": "operations",
    },
    {
        "question": "Average check-in time by day of week",
        "intent": "checkin_time",
        "sql_template": "SELECT strftime('%w', date) as day, AVG(checkin_hour) as avg_hour FROM checkins GROUP BY day ORDER BY day",
        "expected_viz": "bar_chart",
        "category": "operations",
    },
    {
        "question": "How long is the average length of stay?",
        "intent": "avg_stay_length",
        "sql_template": "SELECT AVG(nights) as avg_nights FROM transactions",
        "expected_viz": "metric",
        "category": "operations",
    },
    {
        "question": "What is the most popular meal plan?",
        "intent": "meal_plan_popularity",
        "sql_template": "SELECT meal_plan, COUNT(*) as count FROM transactions GROUP BY meal_plan ORDER BY count DESC",
        "expected_viz": "pie_chart",
        "category": "operations",
    },
    {
        "question": "Show me the booking lead time distribution",
        "intent": "lead_time_distribution",
        "sql_template": "SELECT CASE WHEN lead_time<7 THEN 'Last minute' WHEN lead_time<30 THEN '1-4 weeks' WHEN lead_time<90 THEN '1-3 months' ELSE '3+ months' END as bucket, COUNT(*) FROM bookings GROUP BY bucket",
        "expected_viz": "bar_chart",
        "category": "operations",
    },
    # --- Review / Sentiment ---
    {
        "question": "What is the average review score this month?",
        "intent": "avg_review_score",
        "sql_template": "SELECT AVG(rating) FROM reviews WHERE strftime('%Y-%m', date) = '{current_month}'",
        "expected_viz": "metric",
        "category": "reviews",
    },
    {
        "question": "Show sentiment trend over the last 6 months",
        "intent": "sentiment_trend",
        "sql_template": "SELECT strftime('%Y-%m', date) as month, AVG(rating) as avg_rating, COUNT(*) as review_count FROM reviews WHERE date >= date('now', '-6 months') GROUP BY month ORDER BY month",
        "expected_viz": "line_chart",
        "category": "reviews",
    },
    {
        "question": "What aspects get the most complaints?",
        "intent": "negative_aspects",
        "sql_template": "SELECT 'cleanliness' as aspect, AVG(aspect_cleanliness) as score FROM reviews UNION ALL SELECT 'staff', AVG(aspect_staff) FROM reviews UNION ALL SELECT 'food', AVG(aspect_food) FROM reviews UNION ALL SELECT 'location', AVG(aspect_location) FROM reviews UNION ALL SELECT 'value', AVG(aspect_value) FROM reviews ORDER BY score ASC",
        "expected_viz": "bar_chart",
        "category": "reviews",
    },
    {
        "question": "Compare review scores between hotels",
        "intent": "review_by_hotel",
        "sql_template": "SELECT hotel, AVG(rating) as avg_rating, COUNT(*) as count FROM reviews GROUP BY hotel",
        "expected_viz": "bar_chart",
        "category": "reviews",
    },
    {
        "question": "What do business travelers think about our hotel?",
        "intent": "review_by_trip_type",
        "sql_template": "SELECT trip_type, AVG(rating) as avg_rating, COUNT(*) as count FROM reviews WHERE trip_type='Business' GROUP BY trip_type",
        "expected_viz": "metric",
        "category": "reviews",
    },
    # --- Forecasting / Prediction ---
    {
        "question": "What is the predicted cancellation rate for next month?",
        "intent": "predict_cancellation",
        "sql_template": None,
        "expected_viz": "metric",
        "category": "prediction",
    },
    {
        "question": "Which bookings are at high risk of cancellation?",
        "intent": "high_risk_bookings",
        "sql_template": None,
        "expected_viz": "table",
        "category": "prediction",
    },
    {
        "question": "Predict the revenue for next quarter",
        "intent": "predict_revenue",
        "sql_template": None,
        "expected_viz": "metric",
        "category": "prediction",
    },
    {
        "question": "Which customers are likely to churn in the next 3 months?",
        "intent": "predict_churn",
        "sql_template": None,
        "expected_viz": "table",
        "category": "prediction",
    },
    # --- Summary / General ---
    {
        "question": "Give me an executive summary of last month",
        "intent": "executive_summary",
        "sql_template": None,
        "expected_viz": "text",
        "category": "summary",
    },
    {
        "question": "What are the key KPIs for this quarter?",
        "intent": "quarterly_kpis",
        "sql_template": None,
        "expected_viz": "dashboard",
        "category": "summary",
    },
    {
        "question": "How are we performing compared to last year?",
        "intent": "yoy_comparison",
        "sql_template": None,
        "expected_viz": "table",
        "category": "summary",
    },
    {
        "question": "What are the top 3 areas we need to improve?",
        "intent": "improvement_areas",
        "sql_template": None,
        "expected_viz": "text",
        "category": "summary",
    },
    # --- Additional variations ---
    {
        "question": "Show bookings by market segment",
        "intent": "bookings_by_market",
        "sql_template": "SELECT market_segment, COUNT(*) as bookings FROM bookings GROUP BY market_segment ORDER BY bookings DESC",
        "expected_viz": "bar_chart",
        "category": "operations",
    },
    {
        "question": "What is the no-show rate?",
        "intent": "no_show_rate",
        "sql_template": "SELECT COUNT(CASE WHEN is_no_show=1 THEN 1 END)*100.0/COUNT(*) FROM bookings",
        "expected_viz": "metric",
        "category": "operations",
    },
    {
        "question": "Revenue per available room (RevPAR) trend",
        "intent": "revpar_trend",
        "sql_template": "SELECT date, revpar FROM daily_metrics ORDER BY date DESC LIMIT 90",
        "expected_viz": "line_chart",
        "category": "revenue",
    },
    {
        "question": "Show me the distribution of room types booked",
        "intent": "room_type_distribution",
        "sql_template": "SELECT room_type, COUNT(*) as count FROM transactions GROUP BY room_type ORDER BY count DESC",
        "expected_viz": "pie_chart",
        "category": "operations",
    },
    {
        "question": "What is our customer retention rate?",
        "intent": "retention_rate",
        "sql_template": "SELECT COUNT(DISTINCT CASE WHEN visit_count>1 THEN customer_id END)*100.0/COUNT(DISTINCT customer_id) FROM customer_stats",
        "expected_viz": "metric",
        "category": "customer",
    },
    {
        "question": "Average spend per guest by nationality",
        "intent": "spend_by_nationality",
        "sql_template": "SELECT c.country, AVG(t.total_revenue) as avg_spend FROM customers c JOIN transactions t ON c.customer_id=t.customer_id GROUP BY c.country ORDER BY avg_spend DESC LIMIT 15",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
    {
        "question": "How does seasonality affect our bookings?",
        "intent": "seasonality",
        "sql_template": "SELECT strftime('%m', arrival_date) as month, COUNT(*) as bookings FROM bookings GROUP BY month ORDER BY month",
        "expected_viz": "line_chart",
        "category": "operations",
    },
    {
        "question": "What is the most profitable room type?",
        "intent": "profit_by_room",
        "sql_template": "SELECT room_type, SUM(total_revenue) as total, AVG(daily_rate) as avg_rate FROM transactions GROUP BY room_type ORDER BY total DESC",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
    {
        "question": "Show me cancellations by month of the year",
        "intent": "cancellation_monthly",
        "sql_template": "SELECT strftime('%m', arrival_date) as month, COUNT(CASE WHEN is_canceled=1 THEN 1 END) as cancellations FROM bookings GROUP BY month ORDER BY month",
        "expected_viz": "bar_chart",
        "category": "cancellation",
    },
    {
        "question": "What is our best performing booking channel?",
        "intent": "best_channel",
        "sql_template": "SELECT booking_channel, SUM(total_revenue) as revenue, COUNT(*) as bookings FROM transactions GROUP BY booking_channel ORDER BY revenue DESC",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
    {
        "question": "Guest satisfaction score by department",
        "intent": "satisfaction_by_dept",
        "sql_template": "SELECT 'Cleanliness' as dept, AVG(aspect_cleanliness) as score FROM reviews UNION ALL SELECT 'Staff', AVG(aspect_staff) FROM reviews UNION ALL SELECT 'Food', AVG(aspect_food) FROM reviews UNION ALL SELECT 'Value', AVG(aspect_value) FROM reviews ORDER BY score DESC",
        "expected_viz": "bar_chart",
        "category": "reviews",
    },
    {
        "question": "How many bookings did we receive today?",
        "intent": "daily_bookings",
        "sql_template": "SELECT COUNT(*) FROM bookings WHERE booking_date = date('now')",
        "expected_viz": "metric",
        "category": "operations",
    },
    {
        "question": "Show the correlation between price and cancellation",
        "intent": "price_cancellation_corr",
        "sql_template": "SELECT CASE WHEN adr<80 THEN 'Budget' WHEN adr<150 THEN 'Mid-range' ELSE 'Premium' END as price_tier, COUNT(CASE WHEN is_canceled=1 THEN 1 END)*100.0/COUNT(*) as cancel_rate FROM bookings GROUP BY price_tier",
        "expected_viz": "bar_chart",
        "category": "cancellation",
    },
    {
        "question": "What percentage of guests choose half board?",
        "intent": "meal_plan_pct",
        "sql_template": "SELECT meal_plan, COUNT(*)*100.0/(SELECT COUNT(*) FROM transactions) as pct FROM transactions GROUP BY meal_plan ORDER BY pct DESC",
        "expected_viz": "pie_chart",
        "category": "operations",
    },
    {
        "question": "Show me the extra spend distribution",
        "intent": "extra_spend",
        "sql_template": "SELECT CASE WHEN extra_spend<20 THEN 'Low' WHEN extra_spend<60 THEN 'Medium' ELSE 'High' END as tier, COUNT(*) as count FROM transactions GROUP BY tier",
        "expected_viz": "bar_chart",
        "category": "revenue",
    },
]


def main():
    print("Generating analytics Q&A pairs...")
    df = pd.DataFrame(QA_PAIRS)
    df.to_csv(OUTPUT_DIR / "analytics_qa.csv", index=False)

    print(f"  -> {len(df)} Q&A pairs created")
    print(f"\nCategory distribution:")
    print(df["category"].value_counts().to_string())
    print(f"\nVisualization types:")
    print(df["expected_viz"].value_counts().to_string())


if __name__ == "__main__":
    main()
