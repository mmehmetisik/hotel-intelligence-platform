# Raw Data

## Hotel Booking Demand Dataset

This module uses the **Hotel Booking Demand** dataset from Kaggle.

**Source:** https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
**Records:** ~119,390 bookings | **Features:** 32

### How to download

```bash
# Option 1: Kaggle CLI
kaggle datasets download -d jessemostipak/hotel-booking-demand -p data/raw/ --unzip

# Option 2: Manual download
# 1. Go to the link above
# 2. Download hotel_bookings.csv
# 3. Place it in this directory (data/raw/)
```

The file `hotel_bookings.csv` is excluded from git via `.gitignore`.
