"""
Page 2: Customer Intelligence

Features:
- RFM segmentation analysis
- CLTV prediction results
- Customer clustering visualization
- Segment action recommendations
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

st.set_page_config(page_title="Customer Intelligence", page_icon="💰", layout="wide")
apply_theme()
lang = get_current_lang()

st.markdown(f"# {t('cust_title', lang)}")
st.caption("RFM segmentation, CLTV prediction, and behavioral clustering")

# ─────────────── Load Data ───────────────
SYNTHETIC_DIR = ROOT_DIR / "data" / "synthetic"
transactions_path = SYNTHETIC_DIR / "transactions.csv"

if transactions_path.exists():
    df = pd.read_csv(transactions_path)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # ─── KPI Row ───
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(t("total_customers", lang), f"{df['customer_id'].nunique():,}")
    with k2:
        st.metric(t("avg_revenue", lang), f"€{df['total_revenue'].mean():,.0f}")
    with k3:
        st.metric("Avg. Frequency", f"{df.groupby('customer_id').size().mean():.1f}")
    with k4:
        st.metric("Total Revenue", f"€{df['total_revenue'].sum():,.0f}")

    # ─── Tabs ───
    tab1, tab2, tab3 = st.tabs([
        f"📊 {t('rfm_analysis', lang)}",
        f"💎 {t('cltv_prediction', lang)}",
        f"🎯 {t('clustering', lang)}",
    ])

    # ─── Tab 1: RFM ───
    with tab1:
        analysis_date = df["transaction_date"].max() + pd.Timedelta(days=1)
        rfm = df.groupby("customer_id").agg(
            recency=("transaction_date", lambda x: (analysis_date - x.max()).days),
            frequency=("transaction_id", "count"),
            monetary=("total_revenue", "sum"),
        ).reset_index()

        # RFM Scoring (quintiles)
        rfm["R_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
        rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

        # Segment assignment
        def assign_segment(row):
            r, f = row["R_score"], row["F_score"]
            if r >= 4 and f >= 4:
                return "Champion"
            elif r >= 3 and f >= 3:
                return "Loyal"
            elif r >= 4 and f <= 2:
                return "New Customer"
            elif r >= 3 and f <= 2:
                return "Potential"
            elif r <= 2 and f >= 3:
                return "At Risk"
            elif r <= 2 and f <= 2:
                return "Lost"
            else:
                return "Other"

        rfm["segment"] = rfm.apply(assign_segment, axis=1)

        # Segment distribution
        seg_counts = rfm["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]

        c1, c2 = st.columns(2)
        with c1:
            fig = px.pie(
                seg_counts, values="Count", names="Segment",
                title="Customer Segments",
                hole=0.4,
                color_discrete_sequence=[
                    COLORS["primary"], COLORS["accent"], COLORS["info"],
                    COLORS["success"], COLORS["warning"], "#A78BFA", "#EC4899",
                ],
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            seg_stats = rfm.groupby("segment").agg(
                customers=("customer_id", "count"),
                avg_monetary=("monetary", "mean"),
                avg_frequency=("frequency", "mean"),
                avg_recency=("recency", "mean"),
            ).round(1).sort_values("avg_monetary", ascending=False)

            st.dataframe(seg_stats, use_container_width=True)

        # RFM Scatter
        fig = px.scatter(
            rfm, x="recency", y="monetary", size="frequency",
            color="segment", hover_data=["customer_id", "RFM_score"],
            title="RFM Scatter: Recency vs Monetary (size = Frequency)",
            height=500,
        )
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ─── Tab 2: CLTV ───
    with tab2:
        section_header("Customer Lifetime Value Prediction", "BG-NBD + Gamma-Gamma Model")

        # Calculate simple CLTV proxy
        cust_stats = df.groupby("customer_id").agg(
            total_revenue=("total_revenue", "sum"),
            frequency=("transaction_id", "count"),
            avg_order=("total_revenue", "mean"),
            first_purchase=("transaction_date", "min"),
            last_purchase=("transaction_date", "max"),
        ).reset_index()

        cust_stats["tenure_days"] = (cust_stats["last_purchase"] - cust_stats["first_purchase"]).dt.days
        cust_stats["cltv_proxy"] = cust_stats["avg_order"] * cust_stats["frequency"] * (cust_stats["tenure_days"] / 365 + 1)

        # CLTV segments
        cust_stats["cltv_segment"] = pd.qcut(
            cust_stats["cltv_proxy"], 4,
            labels=["Low Value", "Medium Value", "High Value", "VIP"],
        )

        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(
                cust_stats, x="cltv_proxy", nbins=50,
                title="CLTV Distribution",
                color_discrete_sequence=[COLORS["primary"]],
            )
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            seg_cltv = cust_stats.groupby("cltv_segment").agg(
                count=("customer_id", "count"),
                avg_cltv=("cltv_proxy", "mean"),
                total_revenue=("total_revenue", "sum"),
            ).round(0)

            fig = px.bar(
                seg_cltv.reset_index(),
                x="cltv_segment", y="avg_cltv",
                title="Average CLTV by Segment",
                color="cltv_segment",
                color_discrete_sequence=[COLORS["info"], COLORS["accent"], COLORS["warning"], COLORS["primary"]],
            )
            fig.update_layout(height=400, showlegend=False)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        # Top customers
        section_header("Top 10 Highest Value Customers")
        top10 = cust_stats.nlargest(10, "cltv_proxy")[
            ["customer_id", "total_revenue", "frequency", "avg_order", "cltv_proxy", "cltv_segment"]
        ].round(2)
        top10.columns = ["Customer", "Total Revenue", "Purchases", "Avg Order", "CLTV Score", "Segment"]
        st.dataframe(top10, use_container_width=True, hide_index=True)

    # ─── Tab 3: Clustering ───
    with tab3:
        section_header("Behavioral Customer Clustering", "K-Means on spending patterns")

        # Build clustering features
        clust_df = df.groupby("customer_id").agg(
            total_spend=("total_revenue", "sum"),
            avg_spend=("total_revenue", "mean"),
            num_transactions=("transaction_id", "count"),
            avg_nights=("nights", "mean"),
        ).reset_index()

        # Simple K-Means
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans

        features = ["total_spend", "avg_spend", "num_transactions", "avg_nights"]
        X = clust_df[features].fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        n_clusters = st.slider("Number of Clusters", 2, 8, 4)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clust_df["cluster"] = kmeans.fit_predict(X_scaled)
        clust_df["cluster"] = clust_df["cluster"].astype(str)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.scatter(
                clust_df, x="total_spend", y="num_transactions",
                color="cluster", size="avg_spend",
                title="Customer Clusters: Spend vs Frequency",
                height=450,
            )
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            cluster_stats = clust_df.groupby("cluster")[features].mean().round(1)
            cluster_stats["count"] = clust_df.groupby("cluster").size()
            st.dataframe(cluster_stats, use_container_width=True)

        # Radar chart
        fig = go.Figure()
        for cluster_id in sorted(clust_df["cluster"].unique()):
            values = cluster_stats.loc[cluster_id, features].values.tolist()
            # Normalize for radar
            maxvals = cluster_stats[features].max().values
            norm = [v / m if m > 0 else 0 for v, m in zip(values, maxvals)]
            norm.append(norm[0])

            fig.add_trace(go.Scatterpolar(
                r=norm,
                theta=features + [features[0]],
                fill="toself",
                name=f"Cluster {cluster_id}",
            ))
        fig.update_layout(title="Cluster Profiles (Normalized)", height=450)
        apply_plotly_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

else:
    info_box(t("no_data", lang), "warning")

sidebar_info()
