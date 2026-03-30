"""
Alert System

Threshold-based alerting for model and data monitoring:
- Configurable alert rules per metric
- Severity levels (info, warning, critical)
- Alert history tracking
- Alert aggregation and deduplication
"""

import logging
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """A single alert event."""
    id: str
    timestamp: str
    severity: str  # "info", "warning", "critical"
    category: str  # "data_drift", "model_drift", "performance", "system"
    metric: str
    message: str
    current_value: float = 0.0
    threshold: float = 0.0
    acknowledged: bool = False


@dataclass
class AlertRule:
    """Defines a threshold-based alerting rule."""
    name: str
    metric: str
    category: str
    warning_threshold: float
    critical_threshold: float
    direction: str = "above"  # "above" or "below"
    enabled: bool = True


class AlertManager:
    """Manages alert rules, evaluation, and history."""

    def __init__(self):
        self.rules = self._default_rules()
        self.alerts: list[Alert] = []
        self._alert_counter = 0

    def _default_rules(self) -> list[AlertRule]:
        """Default monitoring alert rules."""
        return [
            # Data drift rules
            AlertRule(
                name="Feature Drift Ratio",
                metric="drift_ratio",
                category="data_drift",
                warning_threshold=0.2,
                critical_threshold=0.4,
                direction="above",
            ),
            AlertRule(
                name="High PSI Feature",
                metric="max_psi",
                category="data_drift",
                warning_threshold=0.1,
                critical_threshold=0.2,
                direction="above",
            ),
            # Model performance rules
            AlertRule(
                name="AUC-ROC Drop",
                metric="auc_roc",
                category="model_drift",
                warning_threshold=0.85,
                critical_threshold=0.80,
                direction="below",
            ),
            AlertRule(
                name="F1 Score Drop",
                metric="f1",
                category="model_drift",
                warning_threshold=0.75,
                critical_threshold=0.65,
                direction="below",
            ),
            AlertRule(
                name="Precision Drop",
                metric="precision",
                category="model_drift",
                warning_threshold=0.70,
                critical_threshold=0.60,
                direction="below",
            ),
            AlertRule(
                name="Recall Drop",
                metric="recall",
                category="model_drift",
                warning_threshold=0.70,
                critical_threshold=0.60,
                direction="below",
            ),
            # Prediction distribution rules
            AlertRule(
                name="High Positive Rate",
                metric="positive_rate",
                category="performance",
                warning_threshold=0.5,
                critical_threshold=0.7,
                direction="above",
            ),
        ]

    def add_rule(self, rule: AlertRule):
        """Add a custom alert rule."""
        self.rules.append(rule)

    def evaluate(self, metrics: dict) -> list[Alert]:
        """Evaluate all rules against current metrics. Returns new alerts."""
        new_alerts = []

        for rule in self.rules:
            if not rule.enabled or rule.metric not in metrics:
                continue

            value = float(metrics[rule.metric])
            severity = self._check_threshold(value, rule)

            if severity:
                alert = self._create_alert(rule, value, severity)
                new_alerts.append(alert)

        self.alerts.extend(new_alerts)

        if new_alerts:
            critical = sum(1 for a in new_alerts if a.severity == "critical")
            warning = sum(1 for a in new_alerts if a.severity == "warning")
            logger.warning(f"Generated {len(new_alerts)} alerts ({critical} critical, {warning} warning)")

        return new_alerts

    def _check_threshold(self, value: float, rule: AlertRule) -> Optional[str]:
        """Check if a value violates a rule's thresholds."""
        if rule.direction == "above":
            if value >= rule.critical_threshold:
                return "critical"
            elif value >= rule.warning_threshold:
                return "warning"
        else:  # "below"
            if value <= rule.critical_threshold:
                return "critical"
            elif value <= rule.warning_threshold:
                return "warning"

        return None

    def _create_alert(self, rule: AlertRule, value: float, severity: str) -> Alert:
        """Create a new alert from a rule violation."""
        self._alert_counter += 1
        alert_id = f"ALT-{self._alert_counter:04d}"

        direction_text = "exceeded" if rule.direction == "above" else "fell below"
        threshold = rule.critical_threshold if severity == "critical" else rule.warning_threshold

        message = (
            f"{severity.upper()}: {rule.name} — "
            f"{rule.metric} ({value:.4f}) {direction_text} "
            f"{severity} threshold ({threshold:.4f})"
        )

        return Alert(
            id=alert_id,
            timestamp=datetime.now().isoformat(),
            severity=severity,
            category=rule.category,
            metric=rule.metric,
            message=message,
            current_value=round(value, 4),
            threshold=round(threshold, 4),
        )

    def get_active_alerts(self, severity: Optional[str] = None, category: Optional[str] = None) -> list[Alert]:
        """Get unacknowledged alerts, optionally filtered."""
        alerts = [a for a in self.alerts if not a.acknowledged]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if category:
            alerts = [a for a in alerts if a.category == category]
        return alerts

    def acknowledge(self, alert_id: str):
        """Mark an alert as acknowledged."""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                return True
        return False

    def acknowledge_all(self):
        """Acknowledge all active alerts."""
        count = 0
        for alert in self.alerts:
            if not alert.acknowledged:
                alert.acknowledged = True
                count += 1
        return count

    def get_summary(self) -> dict:
        """Get alert system summary."""
        active = self.get_active_alerts()
        return {
            "total_alerts": len(self.alerts),
            "active_alerts": len(active),
            "critical": len([a for a in active if a.severity == "critical"]),
            "warning": len([a for a in active if a.severity == "warning"]),
            "info": len([a for a in active if a.severity == "info"]),
            "categories": list(set(a.category for a in active)),
        }

    def get_alerts_df(self) -> "pd.DataFrame":
        """Get all alerts as a DataFrame."""
        import pandas as pd
        if not self.alerts:
            return pd.DataFrame()

        return pd.DataFrame([
            {
                "ID": a.id,
                "Time": a.timestamp,
                "Severity": a.severity,
                "Category": a.category,
                "Metric": a.metric,
                "Value": a.current_value,
                "Threshold": a.threshold,
                "Message": a.message,
                "Ack": a.acknowledged,
            }
            for a in self.alerts
        ])

    def clear_history(self):
        """Clear all alert history."""
        self.alerts.clear()
        self._alert_counter = 0
