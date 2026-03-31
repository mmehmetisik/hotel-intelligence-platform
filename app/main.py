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
    st.metric(t("total_bookings", lang), "119,390")
with k2:
    st.metric(t("cancel_rate", lang), "37.04%")
with k3:
    st.metric(t("total_customers", lang), "12,000")
with k4:
    st.metric(t("best_auc", lang), "0.9465")

st.markdown("")

# ─────────────── Module Cards ───────────────
st.markdown(f"### {t('explore_modules', lang)}")
st.markdown("")

modules = [
    ("📊", 'mod1_title', 'mod1_desc', "1_📊_Cancellation_Predictor"),
    ("📄", 'mod2_title', 'mod2_desc', "3_📄_Invoice_Classifier"),
    ("💬", 'mod3_title', 'mod3_desc', "6_💬_Analytics_Chatbot"),
    ("📈", 'mod4_title', 'mod4_desc', "7_📈_MLOps_Monitor"),
]

m1, m2 = st.columns(2)
for i, (col, (icon, title_key, desc_key, page)) in enumerate(zip([m1, m2, None, None], modules)):
    if i < 2:
        with col:
            st.markdown(f"""
            <div class="module-card">
                <div class="module-icon">{icon}</div>
                <h3>{t(title_key, lang)}</h3>
                <p>{t(desc_key, lang)}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Explore →", key=f"btn_{i}", use_container_width=True):
                st.switch_page(f"pages/{page}.py")

st.markdown("")
m3, m4 = st.columns(2)
for i, (col, (icon, title_key, desc_key, page)) in enumerate(zip([m3, m4], modules[2:]), start=2):
    with col:
        st.markdown(f"""
        <div class="module-card">
            <div class="module-icon">{icon}</div>
            <h3>{t(title_key, lang)}</h3>
            <p>{t(desc_key, lang)}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore →", key=f"btn_{i}", use_container_width=True):
            st.switch_page(f"pages/{page}.py")

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

arch_modules = [
    ("Module 1", "Predictive Analytics", COLORS["primary"],
     ["Cancellation Prediction", "CLTV Modeling", "RFM Segmentation", "K-Means Clustering", "SHAP Explainability"]),
    ("Module 2", "LLM & Unstructured Data", COLORS["accent"],
     ["Invoice Classification", "Master Item Cleanup", "Sentiment Analysis", "Aspect-Level NLP"]),
    ("Module 3", "Conversational AI", COLORS["info"],
     ["NL-to-SQL Engine", "Intent Detection", "Insight Generation", "Auto Chart Builder"]),
    ("Module 4", "MLOps & Monitoring", COLORS["success"],
     ["MLflow Tracking", "Drift Detection", "Alert System", "Model Registry", "Health Score"]),
]

arch_html = '<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; margin: 10px 0;">'
for mod_id, mod_name, color, items in arch_modules:
    items_html = "".join(f'<div style="font-size: 0.78rem; color: {COLORS["text_secondary"]}; padding: 2px 0;">◆ {item}</div>' for item in items)
    arch_html += f'''
    <div style="background: {COLORS["surface"]}; border: 1px solid {color}40; border-top: 3px solid {color};
         border-radius: 8px; padding: 14px; text-align: center;">
        <div style="font-size: 0.7rem; color: {color}; font-weight: 600; letter-spacing: 1px;">{mod_id.upper()}</div>
        <div style="font-size: 0.9rem; color: {COLORS["text"]}; font-weight: 600; margin: 6px 0 10px;">{mod_name}</div>
        {items_html}
    </div>'''
arch_html += '</div>'

# Data & Infrastructure layers
arch_html += f'''
<div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
    <div style="background: {COLORS["surface"]}; border: 1px solid {COLORS["border"]}; border-radius: 8px;
         padding: 10px; text-align: center;">
        <div style="font-size: 0.75rem; color: {COLORS["warning"]}; font-weight: 600;">DATA LAYER</div>
        <div style="font-size: 0.8rem; color: {COLORS["text_secondary"]}; margin-top: 4px;">SQLite · Synthetic + Kaggle · 119K+ Records</div>
    </div>
    <div style="background: {COLORS["surface"]}; border: 1px solid {COLORS["border"]}; border-radius: 8px;
         padding: 10px; text-align: center;">
        <div style="font-size: 0.75rem; color: {COLORS["warning"]}; font-weight: 600;">INFRASTRUCTURE</div>
        <div style="font-size: 0.8rem; color: {COLORS["text_secondary"]}; margin-top: 4px;">Docker · GitHub Actions CI · MLflow Server</div>
    </div>
</div>
'''

st.markdown(arch_html, unsafe_allow_html=True)

# ─────────────── Sidebar Footer ───────────────
sidebar_info()
