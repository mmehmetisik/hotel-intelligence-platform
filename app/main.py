"""
Hotel Intelligence Platform — Main Entry Point

Premium Streamlit multi-page dashboard with:
- Strawberry-inspired dark theme
- Multi-language support (EN/TR/DE)
- 8 interactive pages across 4 AI/ML modules
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.theme import apply_theme
from app.i18n import t, LANG_OPTIONS
from app.components import sidebar_info, COLORS

# ─────────────── Page Config ───────────────
st.set_page_config(
    page_title="Hotel Intelligence Platform",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────── Apply Theme ───────────────
apply_theme()

# ─────────────── Language Selector ───────────────
st.sidebar.markdown(
    f'<h2 style="text-align: center; color: {COLORS["primary"]};">🏨 HIP</h2>',
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    f'<p style="text-align: center; color: {COLORS["text_secondary"]}; '
    f'font-size: 0.8rem; margin-top: -10px;">Hotel Intelligence Platform</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

selected_lang = st.sidebar.selectbox(
    "🌍 Language / Dil / Sprache",
    list(LANG_OPTIONS.keys()),
    index=0,
    key="lang_selector",
)
lang = LANG_OPTIONS[selected_lang]
st.session_state["lang"] = lang

st.sidebar.markdown("---")

# ─────────────── Hero Section ───────────────
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">{t('app_title', lang)}</div>
    <div class="hero-subtitle">{t('hero_description', lang)}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────── KPI Metrics ───────────────
st.markdown("")
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(t("total_bookings", lang), "119,390", "+12.4%")
with k2:
    st.metric(t("cancel_rate", lang), "37.04%", "-2.1%")
with k3:
    st.metric(t("total_customers", lang), "12,000", "+8.5%")
with k4:
    st.metric(t("best_auc", lang), "0.9467", "+0.03")

st.markdown("")

# ─────────────── Module Cards ───────────────
st.markdown(f"### {t('explore_modules', lang)}")
st.markdown("")

m1, m2 = st.columns(2)

with m1:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-icon">📊</div>
        <h3>{t('mod1_title', lang)}</h3>
        <p>{t('mod1_desc', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-icon">📄</div>
        <h3>{t('mod2_title', lang)}</h3>
        <p>{t('mod2_desc', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
m3, m4 = st.columns(2)

with m3:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-icon">💬</div>
        <h3>{t('mod3_title', lang)}</h3>
        <p>{t('mod3_desc', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="module-card">
        <div class="module-icon">📈</div>
        <h3>{t('mod4_title', lang)}</h3>
        <p>{t('mod4_desc', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────── Tech Stack ───────────────
st.markdown("")
st.markdown(f"### {t('tech_stack', lang)}")

techs = [
    "Python 3.11", "XGBoost", "LightGBM", "CatBoost", "Scikit-learn",
    "BG-NBD / Gamma-Gamma", "Groq LLaMA 3.3", "SHAP", "Plotly",
    "Streamlit", "MLflow", "Docker", "GitHub Actions", "SQLite",
    "RapidFuzz", "TF-IDF", "diskcache",
]
pills_html = "".join(f'<span class="tech-pill">{t}</span>' for t in techs)
st.markdown(
    f'<div style="text-align: center; margin: 15px 0;">{pills_html}</div>',
    unsafe_allow_html=True,
)

# ─────────────── Architecture ───────────────
st.markdown("")
st.markdown(f"### {t('architecture', lang)}")

st.markdown(f"""
<div class="premium-card">
    <div style="text-align: center; font-family: monospace; font-size: 0.9rem; color: {COLORS['text_secondary']};">
        <pre style="color: {COLORS['text_secondary']}; background: transparent;">
┌─────────────────────────────────────────────────────────────┐
│                  HOTEL INTELLIGENCE PLATFORM                 │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Module 1    │  Module 2    │  Module 3    │  Module 4      │
│  Predictive  │  LLM &       │  Conversa-   │  MLOps &       │
│  Analytics   │  Unstructured│  tional AI   │  Monitoring    │
│              │  Data        │              │                │
│ ◆ Cancel     │ ◆ Invoice    │ ◆ NL-to-SQL  │ ◆ MLflow       │
│   Prediction │   Classify   │ ◆ Intent     │ ◆ Drift        │
│ ◆ CLTV       │ ◆ Item       │   Detection  │   Detection    │
│ ◆ RFM        │   Cleanup    │ ◆ Insight    │ ◆ Alert        │
│ ◆ Clustering │ ◆ Sentiment  │   Generation │   System       │
│ ◆ SHAP       │   Analysis   │ ◆ Auto Chart │ ◆ Model        │
│              │              │              │   Registry     │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Data Layer: SQLite │ Synthetic + Kaggle │ 119K+ Records    │
├─────────────────────┴────────────────────┴──────────────────┤
│  Infrastructure: Docker │ GitHub Actions CI │ MLflow Server  │
└─────────────────────────────────────────────────────────────┘
        </pre>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────── Sidebar Footer ───────────────
sidebar_info()
