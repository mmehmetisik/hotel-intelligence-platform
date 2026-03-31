"""
Page 5: Review Analyzer

Features:
- Sentiment distribution
- Aspect-level analysis (cleanliness, staff, food, location, value)
- Rating trends
- Sample reviews with sentiment
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
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

st.set_page_config(page_title="Review Analyzer", page_icon="⭐", layout="wide")
apply_theme()
lang = get_current_lang()

st.markdown(f"# {t('review_title', lang)}")
st.caption(t("review_desc", lang))

# ─────────────── Load Data ───────────────
SYNTHETIC_DIR = ROOT_DIR / "data" / "synthetic"
reviews_path = SYNTHETIC_DIR / "reviews.csv"

if reviews_path.exists():
    df = pd.read_csv(reviews_path)

    # ─── KPI Row ───
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(t("total_reviews", lang), f"{len(df):,}")
    with k2:
        st.metric(t("avg_rating", lang), f"{df['rating'].mean():.2f} / 5")
    with k3:
        positive = (df["sentiment_true"] == "positive").mean()
        st.metric(t("positive_rate", lang), f"{positive:.0%}")
    with k4:
        st.metric(t("hotels_covered", lang), f"{df['hotel'].nunique()}")

    # ─── Sidebar Filters ───
    st.sidebar.markdown(f"### {t('filters', lang)}")
    selected_hotel = st.sidebar.multiselect(
        t("hotel_filter", lang), df["hotel"].unique().tolist(),
        default=df["hotel"].unique().tolist(),
    )
    selected_sentiment = st.sidebar.multiselect(
        t("sentiment_filter", lang), df["sentiment_true"].unique().tolist(),
        default=df["sentiment_true"].unique().tolist(),
    )

    filtered = df[
        df["hotel"].isin(selected_hotel) &
        df["sentiment_true"].isin(selected_sentiment)
    ]

    # ─── Tabs ───
    tab1, tab2, tab3 = st.tabs([
        f"📊 {t('sentiment_dist', lang)}",
        f"🎯 {t('aspect_analysis', lang)}",
        f"📝 {t('reviews_tab', lang)}",
    ])

    # ─── Tab 1: Sentiment Distribution ───
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            sent_dist = filtered["sentiment_true"].value_counts().reset_index()
            sent_dist.columns = ["Sentiment", "Count"]
            color_map = {"positive": COLORS["success"], "negative": COLORS["danger"], "neutral": COLORS["warning"]}
            fig = px.pie(
                sent_dist, values="Count", names="Sentiment",
                title=t("sentiment_dist", lang),
                hole=0.45,
                color="Sentiment",
                color_discrete_map=color_map,
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            rating_dist = filtered["rating"].value_counts().sort_index().reset_index()
            rating_dist.columns = ["Rating", "Count"]
            fig = px.bar(
                rating_dist, x="Rating", y="Count",
                title=t("rating_distribution", lang),
                color="Rating",
                color_continuous_scale=["#1E2130", COLORS["primary"]],
            )
            fig.update_layout(height=400, showlegend=False)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        # Sentiment by hotel
        if len(selected_hotel) > 1:
            hotel_sent = filtered.groupby(["hotel", "sentiment_true"]).size().reset_index(name="count")
            fig = px.bar(
                hotel_sent, x="hotel", y="count", color="sentiment_true",
                title=t("sentiment_by_hotel", lang),
                barmode="group",
                color_discrete_map=color_map,
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

    # ─── Tab 2: Aspect Analysis ───
    with tab2:
        aspects = ["aspect_cleanliness", "aspect_staff", "aspect_food", "aspect_location", "aspect_value"]
        available_aspects = [a for a in aspects if a in filtered.columns]

        if available_aspects:
            # Average aspect scores
            aspect_means = filtered[available_aspects].mean().reset_index()
            aspect_means.columns = ["Aspect", "Score"]
            aspect_means["Aspect"] = aspect_means["Aspect"].str.replace("aspect_", "").str.title()

            c1, c2 = st.columns(2)
            with c1:
                fig = px.bar(
                    aspect_means.sort_values("Score", ascending=True),
                    x="Score", y="Aspect",
                    orientation="h",
                    title=t("avg_aspect_scores", lang),
                    color="Score",
                    color_continuous_scale=[COLORS["danger"], COLORS["warning"], COLORS["success"]],
                    range_color=[1, 5],
                )
                fig.update_layout(height=400, showlegend=False)
                apply_plotly_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                # Radar chart
                fig = go.Figure()
                categories = aspect_means["Aspect"].tolist()
                values = aspect_means["Score"].tolist()
                values.append(values[0])
                categories.append(categories[0])

                fig.add_trace(go.Scatterpolar(
                    r=values, theta=categories,
                    fill="toself",
                    fillcolor=f"rgba(255, 75, 75, 0.2)",
                    line_color=COLORS["primary"],
                    name="Overall",
                ))
                fig.update_layout(
                    title=t("aspect_radar", lang),
                    polar=dict(radialaxis=dict(range=[0, 5])),
                    height=400,
                )
                apply_plotly_theme(fig)
                st.plotly_chart(fig, use_container_width=True)

            # Aspect by sentiment
            section_header(t("aspect_by_sentiment", lang))
            for sent in ["positive", "negative", "neutral"]:
                sent_data = filtered[filtered["sentiment_true"] == sent]
                if len(sent_data) > 0:
                    means = sent_data[available_aspects].mean().round(2)
                    means.index = [a.replace("aspect_", "").title() for a in means.index]
                    st.markdown(f"**{sent.title()}** ({len(sent_data)} reviews)")
                    st.dataframe(means.to_frame("Avg Score").T, use_container_width=True)
        else:
            info_box(t("aspect_not_found", lang), "warning")

    # ─── Tab 3: Reviews ───
    with tab3:
        section_header(t("browse_reviews", lang))

        sort_by = st.selectbox(t("sort_by", lang), ["rating", "sentiment_true", "hotel"])
        ascending = st.checkbox(t("ascending", lang), value=False)

        display_cols = ["hotel", "rating", "sentiment_true", "review_text"]
        available_display = [c for c in display_cols if c in filtered.columns]

        sorted_df = filtered[available_display].sort_values(sort_by, ascending=ascending).head(50)
        st.dataframe(sorted_df, use_container_width=True, hide_index=True)

else:
    info_box(t("no_data", lang), "warning")

sidebar_info()
