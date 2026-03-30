import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"
MODELS_DIR = ROOT_DIR / "models"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = "hotel-intelligence"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT_DIR / 'data' / 'hotel.db'}")

# LLM Settings
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 1024

# Cache Settings
CACHE_DIR = ROOT_DIR / ".cache"
CACHE_TTL = 3600  # 1 hour

# Random seed for reproducibility
RANDOM_SEED = 42
