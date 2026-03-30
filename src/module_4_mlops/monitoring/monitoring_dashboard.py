"""
Monitoring Dashboard Utilities

Provides data and helper functions for the MLOps monitoring
Streamlit page. Aggregates signals from all monitoring components.
"""

import logging
from typing import Optional
from pathlib import Path

import numpy as np
import pandas as pd

from src.module_4_mlops.monitoring.data_drift import DataDriftMonitor, DriftReport
from src.module_4_mlops.monitoring.model_drift import ModelDriftMonitor, ModelDriftReport
from src.module_4_mlops.monitoring.alerts import AlertManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models"


class MonitoringDashboard:
    """
    Aggregates all monitoring signals into a unified dashboard view.
    Designed for use by Streamlit pages.
    """

    def __init__(self):
        self.data_drift_monitor = DataDriftMonitor()
        self.model_drift_monitor = ModelDriftMonitor()
        self.alert_manager = AlertManager()
        self._initialized = False

    def initialize(
        self,
        reference_data: Optional[pd.DataFrame] = None,
        baseline_metrics: Optional[dict] = None,
    ):
        """Initialize monitors with reference data and baseline metrics."""
        if reference_data is not None:
            self.data_drift_monitor.set_reference(reference_data)

        if baseline_metrics is not None:
            self.model_drift_monitor.set_baseline_from_metrics(baseline_metrics)

        self._initialized = True
        logger.info("Monitoring dashboard initialized")

    def run_full_check(
        self,
        current_data: Optional[pd.DataFrame] = None,
        y_true: Optional[np.ndarray] = None,
        y_proba: Optional[np.ndarray] = None,
        features: Optional[list] = None,
    ) -> dict:
        """
        Run complete monitoring check.
        Returns combined report from all monitors.
        """
        results = {
            "data_drift": None,
            "model_drift": None,
            "alerts": [],
            "summary": {},
        }

        # 1. Data drift check
        if current_data is not None and self.data_drift_monitor.reference_data is not None:
            drift_report = self.data_drift_monitor.analyze(current_data, features)
            results["data_drift"] = drift_report

            # Feed drift metrics to alert system
            alert_metrics = {
                "drift_ratio": drift_report.drift_ratio,
                "max_psi": max(
                    (r.psi for r in drift_report.feature_results), default=0.0
                ),
            }
            self.alert_manager.evaluate(alert_metrics)

        # 2. Model performance check
        if y_true is not None and y_proba is not None:
            self.model_drift_monitor.evaluate(y_true, y_proba)
            model_report = self.model_drift_monitor.check_drift()
            results["model_drift"] = model_report

            # Feed model metrics to alert system
            if self.model_drift_monitor.performance_history:
                latest = self.model_drift_monitor.performance_history[-1]
                model_metrics = {
                    "auc_roc": latest.auc_roc,
                    "f1": latest.f1,
                    "precision": latest.precision,
                    "recall": latest.recall,
                    "positive_rate": latest.positive_rate,
                }
                self.alert_manager.evaluate(model_metrics)

        # 3. Compile alerts
        results["alerts"] = self.alert_manager.get_active_alerts()

        # 4. Summary
        results["summary"] = self._compile_summary(results)

        return results

    def _compile_summary(self, results: dict) -> dict:
        """Compile an executive summary from all monitoring results."""
        summary = {
            "status": "healthy",
            "data_drift_severity": "none",
            "model_drift_severity": "none",
            "active_alerts": len(results.get("alerts", [])),
            "recommendations": [],
        }

        # Data drift
        if results["data_drift"]:
            summary["data_drift_severity"] = results["data_drift"].overall_severity
            if results["data_drift"].overall_severity in ("warning", "critical"):
                summary["status"] = "degraded"
                summary["recommendations"].append(
                    f"Data drift detected: {results['data_drift'].drifted_features}/"
                    f"{results['data_drift'].total_features} features drifted"
                )

        # Model drift
        if results["model_drift"]:
            summary["model_drift_severity"] = results["model_drift"].severity
            if results["model_drift"].degradation_detected:
                summary["status"] = "degraded"
                summary["recommendations"].append(results["model_drift"].recommendation)

        # Critical = action required
        critical_alerts = [a for a in results.get("alerts", []) if a.severity == "critical"]
        if critical_alerts:
            summary["status"] = "critical"
            summary["recommendations"].insert(0, "CRITICAL alerts require immediate attention")

        if not summary["recommendations"]:
            summary["recommendations"].append("All systems operating normally")

        return summary

    def get_health_score(self) -> dict:
        """
        Calculate an overall system health score (0-100).
        Aggregates data drift, model performance, and alert status.
        """
        score = 100
        components = {}

        # Data drift component (40 points)
        if self.data_drift_monitor.drift_history:
            latest_drift = self.data_drift_monitor.drift_history[-1]
            drift_penalty = min(latest_drift.drift_ratio * 100, 40)
            data_score = max(40 - drift_penalty, 0)
        else:
            data_score = 40  # No drift data = assume healthy
        components["data_quality"] = round(data_score, 1)

        # Model performance component (40 points)
        if self.model_drift_monitor.performance_history and self.model_drift_monitor.baseline_metrics:
            latest = self.model_drift_monitor.performance_history[-1]
            baseline = self.model_drift_monitor.baseline_metrics
            if baseline.auc_roc > 0:
                perf_ratio = latest.auc_roc / baseline.auc_roc
                model_score = min(perf_ratio * 40, 40)
            else:
                model_score = 40
        else:
            model_score = 40  # No performance data = assume healthy
        components["model_performance"] = round(model_score, 1)

        # Alert component (20 points)
        active = self.alert_manager.get_active_alerts()
        critical_count = sum(1 for a in active if a.severity == "critical")
        warning_count = sum(1 for a in active if a.severity == "warning")
        alert_penalty = critical_count * 10 + warning_count * 3
        alert_score = max(20 - alert_penalty, 0)
        components["system_health"] = round(alert_score, 1)

        score = sum(components.values())

        return {
            "overall_score": round(score, 1),
            "status": "healthy" if score >= 80 else "warning" if score >= 60 else "critical",
            "components": components,
        }

    def get_performance_chart_data(self) -> pd.DataFrame:
        """Get performance trend data for Plotly charts."""
        return self.model_drift_monitor.get_performance_trend()

    def get_drift_chart_data(self) -> Optional[pd.DataFrame]:
        """Get latest drift report as DataFrame for visualization."""
        if not self.data_drift_monitor.drift_history:
            return None
        latest = self.data_drift_monitor.drift_history[-1]
        return self.data_drift_monitor.get_drift_summary_df(latest)

    def get_alerts_df(self) -> pd.DataFrame:
        """Get all alerts as DataFrame."""
        return self.alert_manager.get_alerts_df()
