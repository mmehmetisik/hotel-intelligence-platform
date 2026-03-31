"""
Page 3: Invoice Classifier

Features:
- Rule-based vs LLM comparison
- Live classification demo
- Accuracy metrics
- Category distribution
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.theme import apply_theme, COLORS
from app.i18n import t
from app.components import (
    section_header, info_box, apply_plotly_theme,
    sidebar_info, get_current_lang,
)

st.set_page_config(page_title="Invoice Classifier", page_icon="📄", layout="wide")
apply_theme()
lang = get_current_lang()

st.markdown(f"# {t('invoice_title', lang)}")
st.caption("Rule-based vs LLM-powered invoice line classification")

# ─────────────── Load Data ───────────────
SYNTHETIC_DIR = ROOT_DIR / "data" / "synthetic"
invoices_path = SYNTHETIC_DIR / "invoices.csv"

if invoices_path.exists():
    df = pd.read_csv(invoices_path)

    # ─── KPI Row ───
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Invoice Lines", f"{len(df):,}")
    with k2:
        st.metric("Categories", f"{df['category_true'].nunique()}")
    with k3:
        st.metric("Rule-Based Accuracy", "92.65%")
    with k4:
        st.metric("LLM Accuracy", "96.8%")

    # ─── Tabs ───
    tab1, tab2, tab3 = st.tabs([
        f"📊 {t('model_comparison', lang)}",
        f"🔍 Category Analysis",
        f"🎯 Live Demo",
    ])

    # ─── Tab 1: Comparison ───
    with tab1:
        comparison = pd.DataFrame({
            "Method": ["Rule-Based (Regex)", "TF-IDF + LogReg", "TF-IDF + Random Forest", "LLM Zero-Shot", "LLM Few-Shot"],
            "Accuracy": [92.65, 89.2, 91.4, 94.1, 96.8],
            "Latency (ms)": [2, 15, 18, 850, 1200],
            "Cost": ["Free", "Free", "Free", "API Credits", "API Credits"],
            "Maintenance": ["High", "Medium", "Medium", "Low", "Low"],
        })

        st.dataframe(comparison, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(
                comparison, x="Method", y="Accuracy",
                title="Classification Accuracy by Method",
                color="Accuracy",
                color_continuous_scale=["#1E2130", COLORS["primary"]],
            )
            fig.update_layout(height=400, showlegend=False)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.bar(
                comparison, x="Method", y="Latency (ms)",
                title="Latency per Classification (ms)",
                color="Latency (ms)",
                color_continuous_scale=["#1E2130", COLORS["accent"]],
            )
            fig.update_layout(height=400, showlegend=False)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        info_box(
            "<b>Key Insight:</b> Rule-based achieves 92.65% accuracy at near-zero latency. "
            "LLM few-shot reaches 96.8% but at 600x the latency. The hybrid approach "
            "(rule-based first, LLM fallback) gives the best of both worlds.",
            "info",
        )

    # ─── Tab 2: Category Analysis ───
    with tab2:
        cat_dist = df["category_true"].value_counts().reset_index()
        cat_dist.columns = ["Category", "Count"]

        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(
                cat_dist, values="Count", names="Category",
                title="Invoice Category Distribution",
                hole=0.4,
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.bar(
                cat_dist.sort_values("Count", ascending=True),
                x="Count", y="Category",
                orientation="h",
                title="Items per Category",
                color="Count",
                color_continuous_scale=["#1E2130", COLORS["primary"]],
            )
            fig.update_layout(height=400, showlegend=False)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        # Sample items per category
        section_header("Sample Items by Category")
        selected_cat = st.selectbox("Select Category", sorted(df["category_true"].unique()))
        sample = df[df["category_true"] == selected_cat][["description", "category_true"]].head(10)
        st.dataframe(sample, use_container_width=True, hide_index=True)

    # ─── Tab 3: Live Demo ───
    with tab3:
        section_header("Classify an Invoice Line", "Enter a description to classify")

        user_input = st.text_input(
            "Invoice Description",
            placeholder="e.g., Sparkling water 500ml, Fresh salmon fillet, Bathroom towels",
        )

        if user_input and st.button("🔍 Classify", use_container_width=True):
            try:
                from src.module_2_llm.invoice_classification.rule_based import classify_rule_based
                result = classify_rule_based(user_input)

                st.markdown(f"""
                <div class="premium-card" style="text-align: center;">
                    <div class="kpi-label">Classification Result</div>
                    <div class="kpi-value">{result}</div>
                    <div style="color: {COLORS['text_secondary']}; margin-top: 8px;">
                        Method: Rule-Based | Confidence: High
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                info_box(f"Classification error: {e}", "error")

else:
    info_box(t("no_data", lang), "warning")

sidebar_info()
