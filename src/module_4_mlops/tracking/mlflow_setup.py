"""
MLflow Server Setup & Configuration

Provides centralized MLflow experiment management:
- Experiment creation and retrieval
- Tracking URI configuration
- Artifact store configuration
"""

import os
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
DEFAULT_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", f"file:///{ROOT_DIR / 'mlruns'}")
DEFAULT_ARTIFACT_ROOT = str(ROOT_DIR / "mlruns" / "artifacts")


class MLflowSetup:
    """Manages MLflow configuration and experiment lifecycle."""

    def __init__(
        self,
        tracking_uri: Optional[str] = None,
        experiment_name: str = "hotel-intelligence",
    ):
        self.tracking_uri = tracking_uri or DEFAULT_TRACKING_URI
        self.experiment_name = experiment_name
        self.mlflow = None
        self._initialized = False
        self._init_mlflow()

    def _init_mlflow(self):
        """Initialize MLflow with tracking URI."""
        try:
            import mlflow
            self.mlflow = mlflow
            mlflow.set_tracking_uri(self.tracking_uri)
            logger.info(f"MLflow tracking URI: {self.tracking_uri}")
            self._initialized = True
        except ImportError:
            logger.warning("mlflow not installed. Tracking disabled.")

    @property
    def is_available(self) -> bool:
        return self._initialized and self.mlflow is not None

    def get_or_create_experiment(self, name: Optional[str] = None) -> Optional[str]:
        """Get or create an MLflow experiment by name. Returns experiment ID."""
        if not self.is_available:
            return None

        exp_name = name or self.experiment_name
        experiment = self.mlflow.get_experiment_by_name(exp_name)

        if experiment is None:
            exp_id = self.mlflow.create_experiment(
                exp_name,
                artifact_location=DEFAULT_ARTIFACT_ROOT,
            )
            logger.info(f"Created experiment '{exp_name}' (ID: {exp_id})")
        else:
            exp_id = experiment.experiment_id
            logger.info(f"Using experiment '{exp_name}' (ID: {exp_id})")

        self.mlflow.set_experiment(exp_name)
        return exp_id

    def list_experiments(self) -> list:
        """List all experiments."""
        if not self.is_available:
            return []
        experiments = self.mlflow.search_experiments()
        return [
            {
                "id": exp.experiment_id,
                "name": exp.name,
                "artifact_location": exp.artifact_location,
                "lifecycle_stage": exp.lifecycle_stage,
            }
            for exp in experiments
        ]

    def get_best_run(self, experiment_name: Optional[str] = None, metric: str = "auc_roc") -> Optional[dict]:
        """Get the best run from an experiment by a metric."""
        if not self.is_available:
            return None

        exp_name = experiment_name or self.experiment_name
        experiment = self.mlflow.get_experiment_by_name(exp_name)
        if experiment is None:
            return None

        runs = self.mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=[f"metrics.{metric} DESC"],
            max_results=1,
        )

        if runs.empty:
            return None

        best = runs.iloc[0]
        return {
            "run_id": best["run_id"],
            "metrics": {
                col.replace("metrics.", ""): best[col]
                for col in runs.columns if col.startswith("metrics.")
            },
            "params": {
                col.replace("params.", ""): best[col]
                for col in runs.columns if col.startswith("params.")
            },
        }

    def cleanup_old_runs(self, experiment_name: Optional[str] = None, keep_top_n: int = 10):
        """Delete old runs, keeping only top N by AUC-ROC."""
        if not self.is_available:
            return

        exp_name = experiment_name or self.experiment_name
        experiment = self.mlflow.get_experiment_by_name(exp_name)
        if experiment is None:
            return

        runs = self.mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["metrics.auc_roc DESC"],
        )

        if len(runs) > keep_top_n:
            runs_to_delete = runs.iloc[keep_top_n:]
            for _, run in runs_to_delete.iterrows():
                self.mlflow.delete_run(run["run_id"])
            logger.info(f"Cleaned up {len(runs_to_delete)} old runs")

    def get_status(self) -> dict:
        """Get MLflow system status."""
        return {
            "available": self.is_available,
            "tracking_uri": self.tracking_uri,
            "experiment_name": self.experiment_name,
            "experiments": self.list_experiments() if self.is_available else [],
        }
