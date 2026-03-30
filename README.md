# Hotel Intelligence Platform

> End-to-end AI/ML platform for hospitality analytics — from predictive models to conversational AI

[![CI Pipeline](https://github.com/mmehmetisik/hotel-intelligence-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/mmehmetisik/hotel-intelligence-platform/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

## What is this?

A comprehensive AI/ML platform designed for hotel chains, covering the full data science lifecycle: from predictive analytics and LLM-powered data processing to conversational AI and MLOps. Built with production-ready code quality, modular architecture, and real-world business impact focus.

## Modules

| Module | Description | Key Tech |
|--------|-------------|----------|
| **Predictive Analytics** | Booking cancellation prediction, CLTV forecasting, customer segmentation | XGBoost, LightGBM, btyd |
| **LLM & Unstructured Data** | Invoice classification, master item cleanup, review analysis | Groq API, Transformers |
| **Conversational AI** | Natural language hotel analytics assistant with NL-to-SQL | Groq, Streamlit Chat |
| **MLOps & Production** | Experiment tracking, model monitoring, CI/CD pipeline | MLflow, GitHub Actions |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mmehmetisik/hotel-intelligence-platform.git
cd hotel-intelligence-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/main.py
```

### Docker

```bash
docker-compose up --build
```

## Project Structure

```
hotel-intelligence-platform/
├── src/
│   ├── module_1_predictive/    # ML models (cancellation, CLTV, segmentation)
│   ├── module_2_llm/           # LLM pipelines (invoice, cleanup, reviews)
│   ├── module_3_conversational/ # Analytics chatbot (NL-to-SQL)
│   └── module_4_mlops/         # MLflow tracking & monitoring
├── app/                        # Streamlit web application
├── data/                       # Raw, processed & synthetic data
├── notebooks/                  # Kaggle notebooks
├── tests/                      # Unit & integration tests
└── docs/                       # Documentation
```

## Tech Stack

**ML:** Scikit-learn, XGBoost, LightGBM, CatBoost, btyd
**LLM:** Groq API, HuggingFace Transformers, Sentence-Transformers
**App:** Streamlit, Plotly, SQLAlchemy
**MLOps:** MLflow, GitHub Actions, Docker
**Data:** Pandas, NumPy, Faker (synthetic data generation)

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

**Mehmet Isik** — Data Scientist
- GitHub: [@mmehmetisik](https://github.com/mmehmetisik)
