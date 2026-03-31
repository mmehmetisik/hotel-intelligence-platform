"""
Page 4: Master Item Cleanup

Features:
- Fuzzy matching pipeline demo
- Hybrid pipeline visualization (4 layers)
- Match quality analysis
- Live matching demo
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.theme import apply_theme, COLORS
from app.i18n import t
from app.components import (
    section_header, info_box, apply_plotly_theme,
    sidebar_info, get_current_lang,
)

st.set_page_config(page_title="Item Cleanup", page_icon="🔍", layout="wide")
apply_theme()
lang = get_current_lang()

st.markdown("# Master Item Cleanup")
st.caption("4-layer hybrid matching pipeline: Exact → Fuzzy → TF-IDF Embedding → Fuzzy Relaxed")

# ─────────────── Load Data ───────────────
SYNTHETIC_DIR = ROOT_DIR / "data" / "synthetic"
master_path = SYNTHETIC_DIR / "master_items.csv"

if master_path.exists():
    df = pd.read_csv(master_path)

    # ─── KPI Row ───
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Dirty Items", f"{len(df):,}")
    with k2:
        st.metric("Standard Items", f"{df['standard_name'].nunique()}")
    with k3:
        st.metric("Categories", f"{df['category'].nunique()}")
    with k4:
        st.metric("Pipeline Layers", "4")

    # ─── Tabs ───
    tab1, tab2, tab3 = st.tabs([
        "🔄 Pipeline Overview",
        "📊 Match Analysis",
        "🎯 Live Matching",
    ])

    # ─── Tab 1: Pipeline Overview ───
    with tab1:
        # Pipeline architecture
        st.markdown(f"""
        <div class="premium-card">
            <h4 style="color: {COLORS['primary']};">4-Layer Hybrid Matching Pipeline</h4>
            <div style="font-family: monospace; font-size: 0.85rem; line-height: 2;">
                <span style="color: {COLORS['success']};">Layer 1</span> → <b>Exact Match</b> — Direct string comparison after normalization<br>
                <span style="color: {COLORS['info']};">Layer 2</span> → <b>Fuzzy Match (threshold=82)</b> — RapidFuzz WRatio for close matches<br>
                <span style="color: {COLORS['accent']};">Layer 3</span> → <b>TF-IDF Embedding</b> — Character n-gram cosine similarity<br>
                <span style="color: {COLORS['primary']};">Layer 4</span> → <b>Fuzzy Relaxed (threshold=60)</b> — Catch remaining abbreviations
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Simulated layer performance
        layer_data = pd.DataFrame({
            "Layer": ["1. Exact", "2. Fuzzy (82)", "3. TF-IDF", "4. Fuzzy (60)", "Unmatched"],
            "Items Matched": [320, 485, 280, 95, 20],
            "Accuracy": [100.0, 96.5, 93.2, 85.0, 0.0],
        })

        c1, c2 = st.columns(2)
        with c1:
            fig = px.funnel(
                layer_data[layer_data["Items Matched"] > 0],
                x="Items Matched", y="Layer",
                title="Pipeline Funnel: Items Matched per Layer",
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.bar(
                layer_data[layer_data["Accuracy"] > 0],
                x="Layer", y="Accuracy",
                title="Match Accuracy by Layer",
                color="Accuracy",
                color_continuous_scale=["#1E2130", COLORS["success"]],
                text="Accuracy",
            )
            fig.update_layout(height=400, showlegend=False)
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

    # ─── Tab 2: Match Analysis ───
    with tab2:
        section_header("Category Distribution")

        cat_dist = df["category"].value_counts().reset_index()
        cat_dist.columns = ["Category", "Count"]

        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(
                cat_dist, values="Count", names="Category",
                title="Items by Category", hole=0.4,
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Dirty vs Standard name examples
            section_header("Dirty → Standard Mapping Examples")
            sample = df.sample(min(10, len(df)), random_state=42)[["dirty_name", "standard_name", "category"]]
            sample.columns = ["Dirty Name", "Standard Name", "Category"]
            st.dataframe(sample, use_container_width=True, hide_index=True)

    # ─── Tab 3: Live Matching ───
    with tab3:
        section_header("Test the Matching Pipeline", "Enter a dirty product name")

        user_input = st.text_input(
            "Dirty Item Name",
            placeholder="e.g., spag bol, chkn brst, org juce",
        )

        threshold = st.slider("Fuzzy Match Threshold", 30, 100, 70)

        if user_input and st.button("🔍 Find Match", use_container_width=True):
            try:
                from rapidfuzz import fuzz
                standard_items = df["standard_name"].unique().tolist()

                # Find best match
                best_match = None
                best_score = 0
                for item in standard_items:
                    score = fuzz.WRatio(user_input.lower(), item.lower())
                    if score > best_score:
                        best_score = score
                        best_match = item

                if best_score >= threshold:
                    color = COLORS["success"] if best_score >= 80 else COLORS["warning"]
                    st.markdown(f"""
                    <div class="premium-card" style="text-align: center;">
                        <div class="kpi-label">Best Match</div>
                        <div class="kpi-value" style="color: {color};">{best_match}</div>
                        <div style="color: {COLORS['text_secondary']}; margin-top: 8px;">
                            Confidence: {best_score:.0f}% | Input: "{user_input}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Show top 5 matches
                    matches = []
                    for item in standard_items:
                        score = fuzz.WRatio(user_input.lower(), item.lower())
                        matches.append({"Standard Item": item, "Score": score})
                    top5 = pd.DataFrame(matches).nlargest(5, "Score")
                    st.dataframe(top5, use_container_width=True, hide_index=True)
                else:
                    info_box(f"No match found above threshold ({threshold}%). Best: {best_match} ({best_score:.0f}%)", "warning")

            except ImportError:
                info_box("rapidfuzz not installed. Run: pip install rapidfuzz", "error")

else:
    info_box(t("no_data", lang), "warning")

sidebar_info()
