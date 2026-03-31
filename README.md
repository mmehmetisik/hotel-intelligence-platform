# Hotel Intelligence Platform

> End-to-end AI/ML platform for hospitality analytics — from predictive models to conversational AI

[![CI Pipeline](https://github.com/mmehmetisik/hotel-intelligence-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/mmehmetisik/hotel-intelligence-platform/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MLflow](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=white)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

---

## Overview

A comprehensive AI/ML platform designed for hotel chains, covering the full data science lifecycle. The platform processes **119,390 bookings**, **12,000 customers**, and **3,000 reviews** through four integrated modules — delivering actionable business insights with a production-ready architecture.

### Key Results

| Metric | Value |
|--------|-------|
| Cancellation Prediction AUC-ROC | **0.9467** (XGBoost) |
| Invoice Classification Accuracy | **96.8%** (LLM Few-Shot) |
| Rule-Based Classification | **92.65%** (near-zero latency) |
| Customer Segments Identified | **6** (RFM-based) |
| Potential Revenue Savings | **€2M+** annually |
| ML Models Trained & Compared | **5** |
| Features Engineered | **62** |
| Languages Supported (UI) | **3** (EN/TR/DE) |

---

## Modules

### Module 1: Predictive Analytics

**Booking cancellation prediction, CLTV modeling, and customer segmentation.**

- **Cancellation Prediction**: 5 models (Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost) with 62 engineered features. Best: XGBoost with AUC-ROC 0.9467.
- **CLTV Modeling**: BG-NBD + Gamma-Gamma probabilistic models for customer lifetime value prediction using the btyd library.
- **RFM Segmentation**: Quintile-based scoring with 6 customer segments (Champion, Loyal, At Risk, Lost, Potential, New).
- **K-Means Clustering**: Behavioral clustering on spending patterns with elbow/silhouette optimization.
- **SHAP Explainability**: Feature importance analysis — top drivers: deposit type, special requests, lead time.

### Module 2: LLM & Unstructured Data

**Invoice classification, master item cleanup, and sentiment analysis.**

- **Invoice Classification**: Hybrid pipeline — rule-based (92.65%) with LLM fallback (96.8%). Includes TF-IDF + ML baselines.
- **Master Item Cleanup**: 4-layer matching: Exact → Fuzzy (RapidFuzz, threshold=82) → TF-IDF char n-gram embedding → Fuzzy relaxed (threshold=60).
- **Review Sentiment Analysis**: Multi-layer approach — rule-based + GradientBoosting ML + aspect-level models (cleanliness, staff, food, location, value).

### Module 3: Conversational AI

**Natural language to SQL chatbot with auto-visualization.**

- **Intent Detection**: LLM + rule-based fallback classifying into 5 intents (sql_query, prediction, recommendation, summary, explanation).
- **NL-to-SQL**: Schema-aware SQL generation with safety validation (blocks DROP/DELETE/INSERT).
- **Insight Generation**: Business context-aware natural language insights from query results.
- **Auto-Visualization**: Detects optimal chart type (bar, line, pie, scatter, histogram, metric, table) and generates Plotly figures.
- **LLM Routing**: 3-layer pipeline — diskcache → Groq API (LLaMA 3.3 70B) → Fallback responses.

### Module 4: MLOps & Monitoring

**Experiment tracking, model registry, drift detection, and alerting.**

- **MLflow Integration**: Experiment tracking with params, metrics, models, feature importance, and dataset metadata.
- **Model Registry**: Version management with stage transitions (None → Staging → Production → Archived). Local joblib fallback.
- **Data Drift Detection**: PSI (Population Stability Index) + KS test with severity classification (none/warning/critical).
- **Model Performance Monitoring**: Rolling AUC/F1 tracking with degradation alerts and retraining triggers.
- **Alert System**: 7 configurable threshold-based rules with acknowledge/filter capabilities.
- **Health Score**: Unified 0-100 score aggregating data quality, model performance, and system health.

---

## Streamlit Dashboard

Premium dark-themed dashboard with **Strawberry-inspired** color palette and **multi-language support** (EN/TR/DE).

| Page | Description |
|------|-------------|
| **Home** | Hero section, KPI cards, module overview, architecture diagram, tech stack |
| **Cancellation Predictor** | Model comparison, SHAP feature importance, live prediction form, business impact |
| **Customer Intelligence** | RFM segmentation, CLTV prediction, K-Means clustering with radar charts |
| **Invoice Classifier** | Rule-based vs LLM comparison, accuracy/latency trade-off, live demo |
| **Item Cleanup** | 4-layer pipeline visualization, fuzzy matching demo |
| **Review Analyzer** | Sentiment distribution, aspect radar chart, hotel filters |
| **Analytics Chatbot** | Split layout (chat + visualization), Groq LLM integration |
| **MLOps Monitor** | Health score, PSI drift charts, performance tracking, alert dashboard |

---

## Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/mmehmetisik/hotel-intelligence-platform.git
cd hotel-intelligence-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install --pre -r requirements.txt

# Generate synthetic data
python data/synthetic/generate_all.py

# Run the Streamlit app
streamlit run app/main.py
```

### Docker

```bash
docker-compose up --build
# App: http://localhost:8501
# MLflow: http://localhost:5000
```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
MLFLOW_TRACKING_URI=http://localhost:5000
```

---

## Project Structure

```
hotel-intelligence-platform/
├── src/
│   ├── module_1_predictive/       # ML models
│   │   ├── cancellation/          #   EDA, features, training, evaluation
│   │   ├── cltv/                  #   BG-NBD, Gamma-Gamma, RFM
│   │   └── clustering/            #   K-Means, feature engineering
│   ├── module_2_llm/              # LLM pipelines
│   │   ├── invoice_classification/ #   Rule-based, LLM, comparison
│   │   ├── master_item_cleanup/   #   Fuzzy match, hybrid pipeline
│   │   └── review_analysis/       #   Sentiment, aspect analysis
│   ├── module_3_conversational/   # Analytics chatbot
│   │   ├── llm/                   #   Groq client, cache, router
│   │   ├── database/              #   Schema, SQLite init
│   │   └── agents/                #   Intent, SQL, insight, chart
│   └── module_4_mlops/            # MLOps
│       ├── tracking/              #   MLflow setup, logger, registry
│       ├── monitoring/            #   Data drift, model drift, alerts
│       └── pipeline/              #   Training pipeline
├── app/                           # Streamlit dashboard
│   ├── main.py                    #   Home page
│   ├── theme.py                   #   Premium CSS theme
│   ├── i18n.py                    #   EN/TR/DE translations
│   ├── components.py              #   Reusable UI components
│   └── pages/                     #   7 module pages
├── data/
│   ├── raw/                       #   Kaggle hotel bookings
│   └── synthetic/                 #   Generated datasets + scripts
├── notebooks/                     # Kaggle-ready notebooks
├── models/                        # Trained models + metadata
├── tests/                         # 188+ tests
├── .github/workflows/ci.yml       # CI/CD pipeline
├── Dockerfile                     # Container config
├── docker-compose.yml             # Multi-service setup
└── requirements.txt               # Dependencies
```

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **ML/DL** | Scikit-learn, XGBoost, LightGBM, CatBoost, SHAP |
| **Statistical** | BG-NBD, Gamma-Gamma (btyd), SciPy |
| **LLM** | Groq API (LLaMA 3.3 70B), diskcache |
| **NLP** | RapidFuzz, TF-IDF, NLTK |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Web App** | Streamlit (multi-page, custom CSS) |
| **MLOps** | MLflow, GitHub Actions CI/CD |
| **Database** | SQLite, SQLAlchemy |
| **Infrastructure** | Docker, Docker Compose |
| **Testing** | pytest (188+ tests), pytest-cov |

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific module tests
python -m pytest tests/test_conversational.py -v  # Module 3
python -m pytest tests/test_mlops.py -v            # Module 4

# With coverage
python -m pytest tests/ --cov=src --cov-report=term-missing
```

**Test Coverage:**
- Data quality: 35 tests
- Cancellation model: 12 tests
- CLTV pipeline: 8 tests
- Invoice classifier: 10 tests
- Conversational AI: 68 tests
- MLOps: 55 tests

---

## Kaggle Notebooks

| Notebook | Description |
|----------|-------------|
| [01 - Cancellation Prediction](notebooks/01_cancellation_prediction.ipynb) | Full EDA → Feature Engineering → 5 Model Comparison → SHAP → Business Impact |
| [02 - Customer Analytics](notebooks/02_customer_analytics.ipynb) | RFM Segmentation → CLTV Modeling → K-Means Clustering |
| [03 - NLP & LLM](notebooks/03_nlp_and_llm.ipynb) | Invoice Classification → Item Cleanup → Sentiment Analysis |
| [04 - Platform Overview](notebooks/04_platform_overview.ipynb) | Complete system architecture walkthrough |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  HOTEL INTELLIGENCE PLATFORM                 │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Module 1    │  Module 2    │  Module 3    │  Module 4      │
│  Predictive  │  LLM &       │  Conversa-   │  MLOps &       │
│  Analytics   │  Unstructured│  tional AI   │  Monitoring    │
│              │  Data        │              │                │
│ • Cancel     │ • Invoice    │ • NL-to-SQL  │ • MLflow       │
│   Prediction │   Classify   │ • Intent     │ • Drift        │
│ • CLTV       │ • Item       │   Detection  │   Detection    │
│ • RFM        │   Cleanup    │ • Insight    │ • Alert        │
│ • Clustering │ • Sentiment  │   Generation │   System       │
│ • SHAP       │   Analysis   │ • Auto Chart │ • Registry     │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Data Layer: SQLite │ Synthetic + Kaggle │ 119K+ Records    │
├─────────────────────┴────────────────────┴──────────────────┤
│  Infrastructure: Docker │ GitHub Actions CI │ MLflow Server  │
└─────────────────────────────────────────────────────────────┘
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Mehmet Isik** — Data Scientist

- GitHub: [@mmehmetisik](https://github.com/mmehmetisik)
