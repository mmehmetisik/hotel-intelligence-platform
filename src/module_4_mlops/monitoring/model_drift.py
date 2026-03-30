"""
Model Performance Drift Monitor

Tracks model performance over time and detects degradation:
- Rolling metric tracking (AUC-ROC, F1, Precision, Recall)
- Performance degradation alerts
- Prediction distribution monitoring
- Retraining trigger recommendations
"""

import numpy as np
import pandas as pd
import logging
from typing import Optional
from dataclasses import dataclass, field
from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score,
    recall_score, accuracy_score,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PerformanceSnapshot:
    """Single point-in-time performance measurement."""
    timestamp: str
    auc_roc: float
    f1: float
    precision: float
    recall: float
    accuracy: float
    n_samples: int
    positive_rate: float
    prediction_mean: float
    prediction_std: float


@dataclass
class ModelDriftReport:
    """Performance drift analysis report."""
    model_name: str = ""
    baseline_auc: float = 0.0
    current_auc: float = 0.0
    auc_drop_pct: float = 0.0
    degradation_detected: bool = False
    severity: str = "none"
    recommendation: str = ""
    history: list = field(default_factory=list)


class ModelDriftMonitor:
    """Monitors model performance degradation over time."""

    # Performance drop thresholds
    WARNING_DROP_PCT = 5.0     # 5% drop → warning
    CRITICAL_DROP_PCT = 10.0   # 10% drop → retrain

    def __init__(self, model_name: str = "cancellation_model"):
        self.model_name = model_name
        self.baseline_metrics = None
        self.performance_history = []

    def set_baseline(self, y_true: np.ndarray, y_proba: np.ndarray):
        """Set baseline performance from test set evaluation."""
        y_pred = (y_proba >= 0.5).astype(int)
        self.baseline_metrics = self._compute_metrics(y_true, y_pred, y_proba)
        logger.info(
            f"Baseline set: AUC={self.baseline_metrics.auc_roc:.4f}, "
            f"F1={self.baseline_metrics.f1:.4f}"
        )

    def set_baseline_from_metrics(self, metrics: dict):
        """Set baseline from a metrics dictionary (e.g., from saved results)."""
        self.baseline_metrics = PerformanceSnapshot(
            timestamp=pd.Timestamp.now().isoformat(),
            auc_roc=metrics.get("auc_roc", 0.0),
            f1=metrics.get("f1", 0.0),
            precision=metrics.get("precision", 0.0),
            recall=metrics.get("recall", 0.0),
            accuracy=metrics.get("accuracy", 0.0),
            n_samples=metrics.get("n_samples", 0),
            positive_rate=metrics.get("positive_rate", 0.0),
            prediction_mean=metrics.get("prediction_mean", 0.0),
            prediction_std=metrics.get("prediction_std", 0.0),
        )

    def evaluate(self, y_true: np.ndarray, y_proba: np.ndarray) -> PerformanceSnapshot:
        """Evaluate model on new data and track performance."""
        y_pred = (y_proba >= 0.5).astype(int)
        snapshot = self._compute_metrics(y_true, y_pred, y_proba)
        self.performance_history.append(snapshot)
        return snapshot

    def check_drift(self) -> ModelDriftReport:
        """Analyze performance drift vs baseline."""
        if self.baseline_metrics is None:
            return ModelDriftReport(
                model_name=self.model_name,
                recommendation="No baseline set. Run set_baseline() first.",
            )

        if not self.performance_history:
            return ModelDriftReport(
                model_name=self.model_name,
                baseline_auc=self.baseline_metrics.auc_roc,
                recommendation="No evaluation data yet.",
            )

        latest = self.performance_history[-1]
        baseline_auc = self.baseline_metrics.auc_roc
        current_auc = latest.auc_roc

        if baseline_auc > 0:
            drop_pct = (baseline_auc - current_auc) / baseline_auc * 100
        else:
            drop_pct = 0.0

        # Determine severity
        if drop_pct >= self.CRITICAL_DROP_PCT:
            severity = "critical"
            degradation = True
            recommendation = (
                f"CRITICAL: AUC dropped {drop_pct:.1f}% from baseline. "
                "Immediate model retraining recommended. "
                "Check for data distribution shifts or new patterns."
            )
        elif drop_pct >= self.WARNING_DROP_PCT:
            severity = "warning"
            degradation = True
            recommendation = (
                f"WARNING: AUC dropped {drop_pct:.1f}% from baseline. "
                "Schedule retraining within the next cycle. "
                "Monitor closely for further degradation."
            )
        else:
            severity = "none"
            degradation = False
            recommendation = (
                f"Model performing within acceptable range "
                f"(AUC drop: {drop_pct:.1f}%). No action needed."
            )

        return ModelDriftReport(
            model_name=self.model_name,
            baseline_auc=round(baseline_auc, 4),
            current_auc=round(current_auc, 4),
            auc_drop_pct=round(drop_pct, 2),
            degradation_detected=degradation,
            severity=severity,
            recommendation=recommendation,
            history=[
                {
                    "timestamp": s.timestamp,
                    "auc_roc": s.auc_roc,
                    "f1": s.f1,
                    "n_samples": s.n_samples,
                }
                for s in self.performance_history
            ],
        )

    def get_performance_trend(self) -> pd.DataFrame:
        """Get performance metrics over time as DataFrame."""
        if not self.performance_history:
            return pd.DataFrame()

        records = []
        for snap in self.performance_history:
            records.append({
                "timestamp": snap.timestamp,
                "AUC-ROC": snap.auc_roc,
                "F1": snap.f1,
                "Precision": snap.precision,
                "Recall": snap.recall,
                "Accuracy": snap.accuracy,
                "Samples": snap.n_samples,
                "Positive Rate": snap.positive_rate,
            })

        df = pd.DataFrame(records)

        # Add baseline as reference
        if self.baseline_metrics:
            df["Baseline AUC"] = self.baseline_metrics.auc_roc

        return df

    def _compute_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: np.ndarray,
    ) -> PerformanceSnapshot:
        """Compute all performance metrics."""
        return PerformanceSnapshot(
            timestamp=pd.Timestamp.now().isoformat(),
            auc_roc=round(float(roc_auc_score(y_true, y_proba)), 4),
            f1=round(float(f1_score(y_true, y_pred)), 4),
            precision=round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
            recall=round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
            accuracy=round(float(accuracy_score(y_true, y_pred)), 4),
            n_samples=len(y_true),
            positive_rate=round(float(np.mean(y_true)), 4),
            prediction_mean=round(float(np.mean(y_proba)), 4),
            prediction_std=round(float(np.std(y_proba)), 4),
        )
