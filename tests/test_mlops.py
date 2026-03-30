"""
Tests for Module 4 — MLOps & Production

Tests cover:
- MLflow setup and experiment management
- Experiment logger (params, metrics, models)
- Model registry (registration, versioning, local fallback)
- Data drift detection (PSI, KS test)
- Model performance drift monitoring
- Alert system (rules, thresholds, history)
- Monitoring dashboard (health score, aggregation)
- Training pipeline integration

All tests use mocks for MLflow to ensure deterministic, offline results.
"""

import sys
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
from dataclasses import asdict

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))


# ─────────────────────── Data Drift Tests ───────────────────────


class TestDataDriftMonitor:
    """Tests for data drift detection."""

    def setup_method(self):
        from src.module_4_mlops.monitoring.data_drift import DataDriftMonitor
        self.monitor = DataDriftMonitor()

        np.random.seed(42)
        self.ref_data = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 1000),
            "adr": np.random.normal(100, 25, 1000),
            "stays": np.random.poisson(3, 1000).astype(float),
        })
        self.monitor.set_reference(self.ref_data)

    def test_set_reference(self):
        """Reference data is stored correctly."""
        assert self.monitor.reference_data is not None
        assert len(self.monitor.reference_data) == 1000

    def test_psi_no_drift(self):
        """PSI is low for identical distributions."""
        np.random.seed(123)
        ref = np.random.normal(100, 30, 5000)
        cur = np.random.normal(100, 30, 5000)
        psi = self.monitor.calculate_psi(ref, cur)
        assert psi < 0.1  # No significant drift

    def test_psi_with_drift(self):
        """PSI is high for different distributions."""
        ref = np.random.normal(100, 30, 500)
        cur = np.random.normal(200, 30, 500)  # Shifted mean
        psi = self.monitor.calculate_psi(ref, cur)
        assert psi > 0.2  # Significant drift

    def test_psi_constant_values(self):
        """PSI handles constant values gracefully."""
        ref = np.ones(100)
        cur = np.ones(100)
        psi = self.monitor.calculate_psi(ref, cur)
        assert psi == 0.0

    def test_check_feature_no_drift(self):
        """Single feature check: no drift."""
        similar = np.random.normal(100, 30, 500)
        result = self.monitor.check_feature_drift("lead_time", similar)
        assert result.severity == "none"

    def test_check_feature_with_drift(self):
        """Single feature check: drift detected."""
        shifted = np.random.normal(200, 30, 500)
        result = self.monitor.check_feature_drift("lead_time", shifted)
        assert result.drift_detected is True
        assert result.severity in ("warning", "critical")

    def test_check_feature_missing(self):
        """Check returns no-drift for missing feature."""
        result = self.monitor.check_feature_drift("nonexistent", np.array([1, 2, 3]))
        assert result.drift_detected is False

    def test_full_analysis_no_drift(self):
        """Full analysis with similar data."""
        current = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 500),
            "adr": np.random.normal(100, 25, 500),
            "stays": np.random.poisson(3, 500).astype(float),
        })
        report = self.monitor.analyze(current)
        assert report.total_features == 3
        assert report.overall_severity in ("none", "minor")

    def test_full_analysis_with_drift(self):
        """Full analysis with drifted data."""
        current = pd.DataFrame({
            "lead_time": np.random.normal(200, 50, 500),  # Shifted
            "adr": np.random.normal(200, 40, 500),        # Shifted
            "stays": np.random.poisson(10, 500).astype(float),  # Shifted
        })
        report = self.monitor.analyze(current)
        assert report.drifted_features > 0
        assert report.overall_severity in ("warning", "critical")

    def test_analysis_specific_features(self):
        """Analysis with specific feature subset."""
        current = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 500),
            "adr": np.random.normal(100, 25, 500),
            "stays": np.random.poisson(3, 500).astype(float),
        })
        report = self.monitor.analyze(current, features=["lead_time"])
        assert report.total_features == 1

    def test_drift_summary_df(self):
        """Drift report converts to DataFrame."""
        current = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 500),
            "adr": np.random.normal(100, 25, 500),
        })
        report = self.monitor.analyze(current, features=["lead_time", "adr"])
        df = self.monitor.get_drift_summary_df(report)
        assert "Feature" in df.columns
        assert "PSI" in df.columns
        assert len(df) == 2

    def test_drift_history(self):
        """Drift history tracks multiple analyses."""
        current = pd.DataFrame({"lead_time": np.random.normal(100, 30, 100)})
        self.monitor.analyze(current, features=["lead_time"])
        self.monitor.analyze(current, features=["lead_time"])
        assert len(self.monitor.drift_history) == 2

    def test_no_reference_data(self):
        """Analysis fails gracefully without reference."""
        from src.module_4_mlops.monitoring.data_drift import DataDriftMonitor
        empty_monitor = DataDriftMonitor()
        report = empty_monitor.analyze(pd.DataFrame({"x": [1, 2]}))
        assert "No reference" in report.summary


# ─────────────────────── Model Drift Tests ───────────────────────


class TestModelDriftMonitor:
    """Tests for model performance drift monitoring."""

    def setup_method(self):
        from src.module_4_mlops.monitoring.model_drift import ModelDriftMonitor
        self.monitor = ModelDriftMonitor()

        np.random.seed(42)
        self.y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1])
        self.y_proba_good = np.array([0.1, 0.2, 0.15, 0.3, 0.8, 0.9, 0.85, 0.7, 0.25, 0.75])
        self.y_proba_bad = np.array([0.5, 0.4, 0.6, 0.55, 0.5, 0.45, 0.55, 0.4, 0.5, 0.5])

    def test_set_baseline(self):
        """Baseline metrics are computed correctly."""
        self.monitor.set_baseline(self.y_true, self.y_proba_good)
        assert self.monitor.baseline_metrics is not None
        assert self.monitor.baseline_metrics.auc_roc > 0.8

    def test_set_baseline_from_metrics(self):
        """Baseline can be set from a metrics dict."""
        self.monitor.set_baseline_from_metrics({"auc_roc": 0.95, "f1": 0.88})
        assert self.monitor.baseline_metrics.auc_roc == 0.95

    def test_evaluate(self):
        """Evaluation computes and stores snapshot."""
        snap = self.monitor.evaluate(self.y_true, self.y_proba_good)
        assert snap.auc_roc > 0
        assert snap.n_samples == 10
        assert len(self.monitor.performance_history) == 1

    def test_no_drift(self):
        """No drift when performance is stable."""
        self.monitor.set_baseline(self.y_true, self.y_proba_good)
        self.monitor.evaluate(self.y_true, self.y_proba_good)
        report = self.monitor.check_drift()
        assert report.degradation_detected is False
        assert report.severity == "none"

    def test_performance_degradation(self):
        """Drift detected when performance drops."""
        self.monitor.set_baseline(self.y_true, self.y_proba_good)
        self.monitor.evaluate(self.y_true, self.y_proba_bad)
        report = self.monitor.check_drift()
        assert report.degradation_detected is True
        assert report.severity in ("warning", "critical")
        assert report.auc_drop_pct > 0

    def test_no_baseline(self):
        """Drift check works without baseline."""
        report = self.monitor.check_drift()
        assert "No baseline" in report.recommendation

    def test_no_evaluations(self):
        """Drift check works without evaluations."""
        self.monitor.set_baseline(self.y_true, self.y_proba_good)
        report = self.monitor.check_drift()
        assert "No evaluation" in report.recommendation

    def test_performance_trend(self):
        """Performance trend DataFrame is generated."""
        self.monitor.set_baseline(self.y_true, self.y_proba_good)
        self.monitor.evaluate(self.y_true, self.y_proba_good)
        self.monitor.evaluate(self.y_true, self.y_proba_bad)
        df = self.monitor.get_performance_trend()
        assert len(df) == 2
        assert "AUC-ROC" in df.columns
        assert "Baseline AUC" in df.columns

    def test_empty_trend(self):
        """Empty trend returns empty DataFrame."""
        df = self.monitor.get_performance_trend()
        assert df.empty


# ─────────────────────── Alert System Tests ───────────────────────


class TestAlertManager:
    """Tests for the alert system."""

    def setup_method(self):
        from src.module_4_mlops.monitoring.alerts import AlertManager
        self.manager = AlertManager()

    def test_default_rules(self):
        """Default rules are loaded."""
        assert len(self.manager.rules) >= 5

    def test_no_alerts_healthy(self):
        """No alerts for healthy metrics."""
        metrics = {"auc_roc": 0.95, "f1": 0.88, "drift_ratio": 0.05}
        alerts = self.manager.evaluate(metrics)
        assert len(alerts) == 0

    def test_warning_alert(self):
        """Warning alert fires at threshold."""
        metrics = {"auc_roc": 0.83}  # Below 0.85 warning
        alerts = self.manager.evaluate(metrics)
        assert len(alerts) == 1
        assert alerts[0].severity == "warning"

    def test_critical_alert(self):
        """Critical alert fires at threshold."""
        metrics = {"auc_roc": 0.75}  # Below 0.80 critical
        alerts = self.manager.evaluate(metrics)
        assert len(alerts) == 1
        assert alerts[0].severity == "critical"

    def test_multiple_alerts(self):
        """Multiple alerts from multiple metrics."""
        metrics = {"auc_roc": 0.75, "f1": 0.60, "drift_ratio": 0.5}
        alerts = self.manager.evaluate(metrics)
        assert len(alerts) >= 2

    def test_above_direction_alert(self):
        """Alert fires for 'above' direction rules."""
        metrics = {"drift_ratio": 0.25}  # Above 0.2 warning
        alerts = self.manager.evaluate(metrics)
        assert len(alerts) == 1
        assert alerts[0].category == "data_drift"

    def test_acknowledge_alert(self):
        """Alert can be acknowledged."""
        metrics = {"auc_roc": 0.75}
        alerts = self.manager.evaluate(metrics)
        alert_id = alerts[0].id
        result = self.manager.acknowledge(alert_id)
        assert result is True
        assert len(self.manager.get_active_alerts()) == 0

    def test_acknowledge_all(self):
        """All alerts can be acknowledged at once."""
        metrics = {"auc_roc": 0.75, "f1": 0.55}
        self.manager.evaluate(metrics)
        count = self.manager.acknowledge_all()
        assert count >= 2
        assert len(self.manager.get_active_alerts()) == 0

    def test_filter_by_severity(self):
        """Alerts can be filtered by severity."""
        metrics = {"auc_roc": 0.75}  # Critical
        self.manager.evaluate(metrics)
        critical = self.manager.get_active_alerts(severity="critical")
        warning = self.manager.get_active_alerts(severity="warning")
        assert len(critical) == 1
        assert len(warning) == 0

    def test_filter_by_category(self):
        """Alerts can be filtered by category."""
        metrics = {"drift_ratio": 0.25}
        self.manager.evaluate(metrics)
        data_alerts = self.manager.get_active_alerts(category="data_drift")
        model_alerts = self.manager.get_active_alerts(category="model_drift")
        assert len(data_alerts) == 1
        assert len(model_alerts) == 0

    def test_summary(self):
        """Summary includes correct counts."""
        metrics = {"auc_roc": 0.75, "drift_ratio": 0.5}
        self.manager.evaluate(metrics)
        summary = self.manager.get_summary()
        assert summary["total_alerts"] >= 2
        assert summary["active_alerts"] >= 2
        assert summary["critical"] >= 1

    def test_alerts_df(self):
        """Alerts export to DataFrame."""
        metrics = {"auc_roc": 0.75}
        self.manager.evaluate(metrics)
        df = self.manager.get_alerts_df()
        assert "Severity" in df.columns
        assert len(df) >= 1

    def test_clear_history(self):
        """Alert history can be cleared."""
        metrics = {"auc_roc": 0.75}
        self.manager.evaluate(metrics)
        self.manager.clear_history()
        assert len(self.manager.alerts) == 0

    def test_add_custom_rule(self):
        """Custom rules can be added."""
        from src.module_4_mlops.monitoring.alerts import AlertRule
        rule = AlertRule(
            name="Custom Check", metric="custom_metric",
            category="custom", warning_threshold=0.5,
            critical_threshold=0.8, direction="above",
        )
        self.manager.add_rule(rule)
        alerts = self.manager.evaluate({"custom_metric": 0.9})
        assert any(a.category == "custom" for a in alerts)


# ─────────────────────── MLflow Setup Tests (Mocked) ───────────────────────


class TestMLflowSetup:
    """Tests for MLflow setup with mocked mlflow."""

    def test_init_without_mlflow(self):
        """Setup degrades gracefully without mlflow."""
        with patch.dict("sys.modules", {"mlflow": None}):
            from importlib import reload
            import src.module_4_mlops.tracking.mlflow_setup as mod
            # Force re-init to test import failure path
            setup = mod.MLflowSetup.__new__(mod.MLflowSetup)
            setup.tracking_uri = "file:///test"
            setup.experiment_name = "test"
            setup.mlflow = None
            setup._initialized = False
            assert not setup.is_available

    def test_status_unavailable(self):
        """Status returns correctly when unavailable."""
        from src.module_4_mlops.tracking.mlflow_setup import MLflowSetup
        setup = MLflowSetup.__new__(MLflowSetup)
        setup.tracking_uri = "file:///test"
        setup.experiment_name = "test"
        setup.mlflow = None
        setup._initialized = False
        status = setup.get_status()
        assert status["available"] is False
        assert status["experiments"] == []


# ─────────────────────── Experiment Logger Tests ───────────────────────


class TestExperimentLogger:
    """Tests for experiment logging."""

    def test_log_params_unavailable(self):
        """Logging params works when MLflow unavailable."""
        from src.module_4_mlops.tracking.experiment_logger import ExperimentLogger
        mock_setup = MagicMock()
        mock_setup.is_available = False
        exp_log = ExperimentLogger(setup=mock_setup)
        # Should not raise
        exp_log.log_params({"lr": 0.01, "depth": 6})

    def test_log_metrics_unavailable(self):
        """Logging metrics works when MLflow unavailable."""
        from src.module_4_mlops.tracking.experiment_logger import ExperimentLogger
        mock_setup = MagicMock()
        mock_setup.is_available = False
        exp_log = ExperimentLogger(setup=mock_setup)
        exp_log.log_metrics({"auc_roc": 0.95, "f1": 0.88})

    def test_get_experiment_history_unavailable(self):
        """History returns empty when MLflow unavailable."""
        from src.module_4_mlops.tracking.experiment_logger import ExperimentLogger
        mock_setup = MagicMock()
        mock_setup.is_available = False
        exp_log = ExperimentLogger(setup=mock_setup)
        df = exp_log.get_experiment_history()
        assert df.empty


# ─────────────────────── Model Registry Tests ───────────────────────


class TestModelRegistry:
    """Tests for model registry."""

    def test_local_model_listing(self):
        """Lists locally saved models."""
        from src.module_4_mlops.tracking.model_registry import ModelRegistry
        registry = ModelRegistry(mlflow_setup=None)
        models = registry.list_models()
        # Should return local models from disk (may be empty or populated)
        assert isinstance(models, list)

    def test_unavailable_register(self):
        """Registration returns None when unavailable."""
        from src.module_4_mlops.tracking.model_registry import ModelRegistry
        registry = ModelRegistry(mlflow_setup=None)
        result = registry.register_model("fake_run", "test_model")
        assert result is None

    def test_unavailable_transition(self):
        """Stage transition returns None when unavailable."""
        from src.module_4_mlops.tracking.model_registry import ModelRegistry
        registry = ModelRegistry(mlflow_setup=None)
        result = registry.transition_stage("model", "1", "Production")
        assert result is None

    def test_get_status(self):
        """Status returns valid structure."""
        from src.module_4_mlops.tracking.model_registry import ModelRegistry
        registry = ModelRegistry(mlflow_setup=None)
        status = registry.get_status()
        assert "registry_available" in status
        assert "models" in status


# ─────────────────────── Monitoring Dashboard Tests ───────────────────────


class TestMonitoringDashboard:
    """Tests for the unified monitoring dashboard."""

    def setup_method(self):
        from src.module_4_mlops.monitoring.monitoring_dashboard import MonitoringDashboard
        self.dashboard = MonitoringDashboard()

        np.random.seed(42)
        self.ref_data = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 500),
            "adr": np.random.normal(100, 25, 500),
        })
        self.baseline_metrics = {
            "auc_roc": 0.94, "f1": 0.86, "precision": 0.82,
            "recall": 0.90, "accuracy": 0.85,
        }

    def test_initialize(self):
        """Dashboard initializes with reference data and baseline."""
        self.dashboard.initialize(self.ref_data, self.baseline_metrics)
        assert self.dashboard._initialized is True
        assert self.dashboard.data_drift_monitor.reference_data is not None
        assert self.dashboard.model_drift_monitor.baseline_metrics is not None

    def test_health_score_healthy(self):
        """Health score is high when no issues."""
        self.dashboard.initialize(self.ref_data, self.baseline_metrics)
        health = self.dashboard.get_health_score()
        assert health["overall_score"] >= 80
        assert health["status"] == "healthy"
        assert "data_quality" in health["components"]
        assert "model_performance" in health["components"]
        assert "system_health" in health["components"]

    def test_health_score_with_alerts(self):
        """Health score drops with critical alerts."""
        self.dashboard.initialize(self.ref_data, self.baseline_metrics)
        # Fire critical alerts
        self.dashboard.alert_manager.evaluate({"auc_roc": 0.5, "f1": 0.3})
        health = self.dashboard.get_health_score()
        assert health["components"]["system_health"] < 20

    def test_full_check_data_only(self):
        """Full check with only data drift."""
        self.dashboard.initialize(self.ref_data, self.baseline_metrics)
        current = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 200),
            "adr": np.random.normal(100, 25, 200),
        })
        results = self.dashboard.run_full_check(current_data=current)
        assert results["data_drift"] is not None
        assert "summary" in results

    def test_full_check_model_only(self):
        """Full check with only model evaluation."""
        self.dashboard.initialize(self.ref_data, self.baseline_metrics)
        y_true = np.array([0, 0, 1, 1, 0, 1, 0, 1])
        y_proba = np.array([0.1, 0.2, 0.8, 0.9, 0.3, 0.7, 0.15, 0.85])
        results = self.dashboard.run_full_check(y_true=y_true, y_proba=y_proba)
        assert results["model_drift"] is not None

    def test_summary_healthy(self):
        """Summary is healthy with good data."""
        self.dashboard.initialize(self.ref_data, self.baseline_metrics)
        current = pd.DataFrame({
            "lead_time": np.random.normal(100, 30, 200),
            "adr": np.random.normal(100, 25, 200),
        })
        results = self.dashboard.run_full_check(current_data=current)
        assert results["summary"]["status"] in ("healthy", "degraded")

    def test_empty_chart_data(self):
        """Chart data returns None when no history."""
        assert self.dashboard.get_drift_chart_data() is None
        assert self.dashboard.get_performance_chart_data().empty

    def test_alerts_df(self):
        """Alerts DataFrame works."""
        df = self.dashboard.get_alerts_df()
        assert isinstance(df, pd.DataFrame)


# ─────────────────────── Training Pipeline Tests ───────────────────────


class TestTrainingPipeline:
    """Tests for the training pipeline (mocked)."""

    def test_load_saved_baseline(self):
        """Pipeline can attempt to load saved baseline."""
        from src.module_4_mlops.pipeline.training_pipeline import TrainingPipeline
        pipeline = TrainingPipeline.__new__(TrainingPipeline)
        pipeline.experiment_name = "test"

        # Mock MODELS_DIR
        with patch("src.module_4_mlops.pipeline.training_pipeline.MODELS_DIR", Path("/nonexistent")):
            result = pipeline.load_saved_baseline()
            assert result is None

    def test_pipeline_status(self):
        """Pipeline status returns valid structure."""
        from src.module_4_mlops.pipeline.training_pipeline import TrainingPipeline
        pipeline = TrainingPipeline.__new__(TrainingPipeline)

        mock_setup = MagicMock()
        mock_setup.get_status.return_value = {"available": False}
        mock_registry = MagicMock()
        mock_registry.get_status.return_value = {"registry_available": False}
        mock_model_monitor = MagicMock()
        mock_model_monitor.baseline_metrics = None

        pipeline.setup = mock_setup
        pipeline.registry = mock_registry
        pipeline.model_drift_monitor = mock_model_monitor

        status = pipeline.get_status()
        assert "mlflow" in status
        assert "registry" in status
        assert "baseline_loaded" in status
