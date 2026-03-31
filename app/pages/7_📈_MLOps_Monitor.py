"""
Page 7: MLOps Monitor

Features:
- System health score (0-100)
- Data drift analysis with PSI/KS
- Model performance tracking
- Alert dashboard
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
    section_header, info_box, apply_plotly_theme, status_badge,
    sidebar_info, get_current_lang,
)

st.set_page_config(page_title="MLOps Monitor", page_icon="📈", layout="wide")
apply_theme()
lang = get_current_lang()

st.markdown(f"# {t('mlops_title', lang)}")
st.caption(t("mlops_desc", lang))

# ─── Initialize Dashboard ───
try:
    from src.module_4_mlops.monitoring.monitoring_dashboard import MonitoringDashboard
    dashboard = MonitoringDashboard()

    np.random.seed(42)
    ref_data = pd.DataFrame({
        "lead_time": np.random.normal(100, 45, 1000),
        "adr": np.random.normal(101, 50, 1000),
        "stays_total": np.random.poisson(3, 1000).astype(float),
        "adults": np.random.choice([1, 2, 3], 1000, p=[0.3, 0.6, 0.1]).astype(float),
        "previous_cancellations": np.random.poisson(0.2, 1000).astype(float),
        "total_of_special_requests": np.random.poisson(1, 1000).astype(float),
    })

    baseline_metrics = {
        "auc_roc": 0.9467, "f1": 0.8734, "precision": 0.8521,
        "recall": 0.8960, "accuracy": 0.8812,
    }

    dashboard.initialize(ref_data, baseline_metrics)
    dashboard_ready = True
except Exception as e:
    dashboard_ready = False
    dashboard_error = str(e)

if dashboard_ready:
    # ─── Tabs (before health score so drift_level is available) ───
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📊 {t('data_drift', lang)}",
        f"📈 {t('model_performance', lang)}",
        f"🔔 {t('alerts', lang)}",
        f"⚙️ {t('experiment_tracking', lang)}",
    ])

    # ─── Tab 1: Data Drift ───
    with tab1:
        section_header(t("data_drift_analysis", lang), t("drift_subtitle", lang))

        drift_level = st.slider(t("simulate_drift", lang), 0.0, 2.0, 0.3, 0.1,
                                help="0 = no drift, 2 = extreme drift")

        np.random.seed(123)
        current_data = pd.DataFrame({
            "lead_time": np.random.normal(100 + drift_level * 30, 45, 500),
            "adr": np.random.normal(101 + drift_level * 20, 50, 500),
            "stays_total": np.random.poisson(3 + drift_level, 500).astype(float),
            "adults": np.random.choice([1, 2, 3], 500, p=[0.3, 0.6, 0.1]).astype(float),
            "previous_cancellations": np.random.poisson(0.2 + drift_level * 0.3, 500).astype(float),
            "total_of_special_requests": np.random.poisson(1, 500).astype(float),
        })

        report = dashboard.data_drift_monitor.analyze(current_data)
        drift_df = dashboard.data_drift_monitor.get_drift_summary_df(report)

        if not drift_df.empty:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(t("features_analyzed", lang), report.total_features)
            with c2:
                st.metric(t("drifted_features", lang), report.drifted_features)
            with c3:
                st.metric(t("overall_severity", lang), report.overall_severity.upper())

            fig = px.bar(
                drift_df.sort_values("PSI", ascending=True),
                x="PSI", y="Feature",
                orientation="h",
                title="Population Stability Index (PSI)",
                color="Severity",
                color_discrete_map={
                    "none": COLORS["success"],
                    "warning": COLORS["warning"],
                    "critical": COLORS["danger"],
                },
            )
            fig.add_vline(x=0.1, line_dash="dash", line_color=COLORS["warning"],
                          annotation_text="Warning (0.1)")
            fig.add_vline(x=0.2, line_dash="dash", line_color=COLORS["danger"],
                          annotation_text="Critical (0.2)")
            fig.update_layout(height=400)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Detailed Drift Report"):
                st.dataframe(drift_df, use_container_width=True, hide_index=True)

    # ─── Tab 2: Model Performance ───
    with tab2:
        section_header(t("perf_tracking", lang), t("perf_subtitle", lang))

        np.random.seed(42)
        n_evals = 10
        perf_degradation = st.slider(t("simulate_degradation", lang), 0.0, 0.15, 0.02, 0.01)

        for i in range(n_evals):
            n = 200
            y_true = np.random.binomial(1, 0.37, n)
            noise = np.random.normal(0, 0.15, n)
            y_proba = np.clip(y_true * 0.7 + (1 - y_true) * 0.3 + noise - (i * perf_degradation * 0.5), 0, 1)
            dashboard.model_drift_monitor.evaluate(y_true, y_proba)

        perf_df = dashboard.get_performance_chart_data()
        drift_report = dashboard.model_drift_monitor.check_drift()

        if not perf_df.empty:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Baseline AUC", f"{drift_report.baseline_auc:.4f}")
            with c2:
                st.metric("Current AUC", f"{drift_report.current_auc:.4f}",
                           delta=f"{-drift_report.auc_drop_pct:.1f}%")
            with c3:
                sev = drift_report.severity
                st.markdown(f"""
                <div class="premium-card" style="text-align: center;">
                    <div class="kpi-label">Status</div>
                    <div>{status_badge(sev if sev != 'none' else 'healthy')}</div>
                </div>
                """, unsafe_allow_html=True)

            fig = go.Figure()
            for metric in ["AUC-ROC", "F1", "Precision", "Recall"]:
                if metric in perf_df.columns:
                    fig.add_trace(go.Scatter(
                        y=perf_df[metric], mode="lines+markers",
                        name=metric,
                    ))

            if "Baseline AUC" in perf_df.columns:
                fig.add_hline(
                    y=perf_df["Baseline AUC"].iloc[0],
                    line_dash="dash", line_color=COLORS["text_muted"],
                    annotation_text="Baseline",
                )

            fig.update_layout(title=t("perf_metrics_time", lang), height=450)
            apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

            if drift_report.recommendation:
                box_type = "error" if "CRITICAL" in drift_report.recommendation else \
                           "warning" if "WARNING" in drift_report.recommendation else "success"
                info_box(drift_report.recommendation, box_type)

    # ─── Tab 3: Alerts ───
    with tab3:
        section_header(t("alert_dashboard", lang), t("alert_subtitle", lang))

        results = dashboard.run_full_check(
            current_data=current_data if 'current_data' in dir() else None,
        )

        alert_summary = dashboard.alert_manager.get_summary()
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.metric(t("alerts", lang), alert_summary["total_alerts"])
        with a2:
            st.metric("Active", alert_summary["active_alerts"])
        with a3:
            st.metric("Critical", alert_summary["critical"])
        with a4:
            st.metric("Warning", alert_summary["warning"])

        alerts_df = dashboard.get_alerts_df()
        if not alerts_df.empty:
            st.dataframe(alerts_df, use_container_width=True, hide_index=True)

            if st.button(f"✅ {t('acknowledge_all', lang)}", use_container_width=True):
                count = dashboard.alert_manager.acknowledge_all()
                st.success(f"Acknowledged {count} alerts")
                st.rerun()
        else:
            info_box(t("no_alerts", lang), "success")

        with st.expander("Alert Rules Configuration"):
            rules_data = []
            for rule in dashboard.alert_manager.rules:
                rules_data.append({
                    "Rule": rule.name,
                    "Metric": rule.metric,
                    "Category": rule.category,
                    "Warning": rule.warning_threshold,
                    "Critical": rule.critical_threshold,
                    "Direction": rule.direction,
                    "Enabled": rule.enabled,
                })
            st.dataframe(pd.DataFrame(rules_data), use_container_width=True, hide_index=True)

    # ─── Tab 4: Experiment Tracking ───
    with tab4:
        section_header(t("experiment_tracking", lang), t("exp_subtitle", lang))

        info_box(
            "MLflow experiment tracking is available when running with a local MLflow server. "
            "Start with: <code>mlflow server --port 5000</code>",
            "info",
        )

        results_path = ROOT_DIR / "models" / "cancellation" / "model_comparison.csv"
        if results_path.exists():
            results_df = pd.read_csv(results_path, index_col=0)
            display_cols = [c for c in ["auc_roc", "f1", "precision", "recall", "accuracy",
                                         "cv_roc_auc", "cv_f1"] if c in results_df.columns]
            st.dataframe(
                results_df[display_cols].round(4).style.highlight_max(axis=0, color=COLORS["primary"]),
                use_container_width=True,
            )

        section_header(t("model_registry", lang))
        st.markdown(f"""
        <div class="premium-card">
            <table style="width: 100%; color: {COLORS['text_secondary']};">
                <tr><td><b>Registry Status</b></td><td>Local Filesystem</td></tr>
                <tr><td><b>Stages</b></td><td>None → Staging → Production → Archived</td></tr>
                <tr><td><b>Versioning</b></td><td>Automatic on registration</td></tr>
                <tr><td><b>Fallback</b></td><td>joblib local models</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    # ─── Health Score (after drift/perf analysis so it reflects current state) ───
    # Recalculate based on drift and performance results
    drift_penalty = 0
    if 'report' in dir() and report.drifted_features > 0:
        drift_penalty = min(report.drifted_features * 10, 40)

    perf_penalty = 0
    if 'drift_report' in dir() and drift_report.auc_drop_pct > 5:
        perf_penalty = min(int(drift_report.auc_drop_pct * 2), 40)

    adjusted_score = max(100 - drift_penalty - perf_penalty, 0)
    adjusted_dq = max(40 - drift_penalty, 0)
    adjusted_mp = max(40 - perf_penalty, 0)
    adjusted_status = "healthy" if adjusted_score >= 80 else "warning" if adjusted_score >= 60 else "critical"

    # Render health score at the top using st.container
    health_container = st.container()
    with health_container:
        h1, h2, h3, h4 = st.columns(4)
        with h1:
            score_color = COLORS["success"] if adjusted_score >= 80 else COLORS["warning"] if adjusted_score >= 60 else COLORS["danger"]
            st.markdown(f"""
            <div class="premium-card" style="text-align: center;">
                <div class="kpi-label">{t('health_score', lang)}</div>
                <div class="kpi-value" style="color: {score_color}; font-size: 2.5rem;">{adjusted_score:.0f}</div>
                <div>{status_badge(adjusted_status)}</div>
            </div>
            """, unsafe_allow_html=True)
        with h2:
            st.metric(t("data_quality", lang), f"{adjusted_dq:.0f}/40")
        with h3:
            st.metric(t("model_performance", lang), f"{adjusted_mp:.0f}/40")
        with h4:
            st.metric(t("system_health", lang), "20/20")

else:
    info_box(f"Dashboard initialization error: {dashboard_error}", "error")

sidebar_info()
