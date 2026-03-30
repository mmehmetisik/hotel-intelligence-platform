-- Hotel Intelligence Platform — Analytics Database Schema

CREATE TABLE IF NOT EXISTS bookings (
    booking_id TEXT PRIMARY KEY,
    hotel TEXT,
    is_canceled INTEGER,
    lead_time INTEGER,
    arrival_date TEXT,
    arrival_date_year INTEGER,
    arrival_date_month TEXT,
    stays_in_weekend_nights INTEGER,
    stays_in_week_nights INTEGER,
    adults INTEGER,
    children REAL,
    babies INTEGER,
    meal TEXT,
    country TEXT,
    market_segment TEXT,
    distribution_channel TEXT,
    is_repeated_guest INTEGER,
    previous_cancellations INTEGER,
    previous_bookings_not_canceled INTEGER,
    deposit_type TEXT,
    customer_type TEXT,
    adr REAL,
    required_car_parking_spaces INTEGER,
    total_of_special_requests INTEGER,
    reservation_status TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT,
    transaction_date TEXT,
    nights INTEGER,
    room_type TEXT,
    daily_rate REAL,
    total_revenue REAL,
    hotel_type TEXT,
    booking_channel TEXT,
    meal_plan TEXT,
    extra_spend REAL
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    country TEXT,
    customer_type TEXT,
    segment_true TEXT
);

CREATE TABLE IF NOT EXISTS customer_segments (
    customer_id TEXT PRIMARY KEY,
    recency INTEGER,
    frequency INTEGER,
    monetary REAL,
    total_revenue REAL,
    R_score INTEGER,
    F_score INTEGER,
    M_score INTEGER,
    RFM_score INTEGER,
    rfm_segment TEXT,
    cltv REAL,
    segment TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT PRIMARY KEY,
    hotel TEXT,
    date TEXT,
    reviewer_country TEXT,
    trip_type TEXT,
    rating INTEGER,
    review_text TEXT,
    sentiment_true TEXT,
    aspect_cleanliness INTEGER,
    aspect_staff INTEGER,
    aspect_food INTEGER,
    aspect_location INTEGER,
    aspect_value INTEGER
);

CREATE TABLE IF NOT EXISTS daily_metrics (
    date TEXT PRIMARY KEY,
    hotel_type TEXT,
    total_rooms INTEGER,
    occupied_rooms INTEGER,
    occupancy_rate REAL,
    revpar REAL,
    adr REAL
);
