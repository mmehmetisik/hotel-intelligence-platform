"""
Experiment Logger

Generic experiment logger that wraps MLflow for tracking:
- Model parameters, metrics, and artifacts
- Feature importance
- Training metadata (dataset size, duration, etc.)
- Model signatures and input examples

Works with any scikit-learn compatible model.
"""

import time
import json
import logging
import tempfile
from pathlib import Path
from typing import Optional, Any

import numpy as np
import pandas as pd

from src.module_4_mlops.tracking.mlflow_setup import MLflowSetup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExperimentLogger:
    """Logs ML experiments to MLflow with rich metadata."""

    def __init__(self, setup: Optional[MLflowSetup] = None):
        self.setup = setup or MLflowSetup()
        self.active_run = None

    @property
    def is_available(self) -> bool:
        return self.setup.is_available

    def start_run(
        self,
        run_name: str,
        experiment_name: Optional[str] = None,
        tags: Optional[dict] = None,
    ) -> Optional[str]:
        """Start a new MLflow run. Returns run_id."""
        if not self.is_available:
            logger.warning("MLflow unavailable. Logging to console only.")
            return None

        mlflow = self.setup.mlflow
        self.setup.get_or_create_experiment(experiment_name)

        self.active_run = mlflow.start_run(run_name=run_name, tags=tags)
        run_id = self.active_run.info.run_id
        logger.info(f"Started run '{run_name}' (ID: {run_id})")
        return run_id

    def end_run(self):
        """End the active run."""
        if self.is_available and self.active_run:
            self.setup.mlflow.end_run()
            self.active_run = None

    def log_params(self, params: dict):
        """Log model hyperparameters."""
        if not self.is_available:
            logger.info(f"[DRY] Params: {params}")
            return

        # MLflow truncates param values > 500 chars
        for key, value in params.items():
            str_value = str(value)[:500]
            self.setup.mlflow.log_param(key, str_value)

    def log_metrics(self, metrics: dict, step: Optional[int] = None):
        """Log evaluation metrics."""
        if not self.is_available:
            logger.info(f"[DRY] Metrics: {metrics}")
            return

        for key, value in metrics.items():
            if isinstance(value, (int, float, np.integer, np.floating)):
                self.setup.mlflow.log_metric(key, float(value), step=step)

    def log_model(self, model: Any, model_name: str, input_example: Optional[pd.DataFrame] = None):
        """Log a trained model as an artifact."""
        if not self.is_available:
            logger.info(f"[DRY] Model: {model_name}")
            return

        try:
            self.setup.mlflow.sklearn.log_model(
                model,
                artifact_path=model_name,
                input_example=input_example,
            )
            logger.info(f"Logged model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to log model: {e}")

    def log_feature_importance(self, model: Any, feature_names: list):
        """Log feature importance as artifact and metrics."""
        if not self.is_available:
            return

        importance = None

        if hasattr(model, "feature_importances_"):
            importance = model.feature_importances_
        elif hasattr(model, "coef_"):
            importance = np.abs(model.coef_[0]) if model.coef_.ndim > 1 else np.abs(model.coef_)

        if importance is None:
            return

        fi_df = pd.DataFrame({
            "feature": feature_names,
            "importance": importance,
        }).sort_values("importance", ascending=False)

        # Log top 20 as metrics
        for _, row in fi_df.head(20).iterrows():
            safe_name = row["feature"][:250].replace(" ", "_")
            self.setup.mlflow.log_metric(f"fi_{safe_name}", float(row["importance"]))

        # Log full table as artifact
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            fi_df.to_csv(f, index=False)
            self.setup.mlflow.log_artifact(f.name, "feature_importance")

    def log_dataset_info(self, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series):
        """Log dataset metadata."""
        info = {
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "n_features": int(X_train.shape[1]),
            "target_rate": float(y_train.mean()),
            "feature_names": X_train.columns.tolist(),
        }

        self.log_params({
            "train_samples": info["train_samples"],
            "test_samples": info["test_samples"],
            "n_features": info["n_features"],
            "target_rate": round(info["target_rate"], 4),
        })

        if self.is_available:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                json.dump(info, f, indent=2)
                self.setup.mlflow.log_artifact(f.name, "dataset_info")

    def log_confusion_matrix(self, cm: list):
        """Log confusion matrix as artifact."""
        if not self.is_available:
            return

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"confusion_matrix": cm}, f)
            self.setup.mlflow.log_artifact(f.name, "evaluation")

    def log_training_run(
        self,
        model: Any,
        model_name: str,
        params: dict,
        metrics: dict,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        feature_names: list,
        confusion_matrix: Optional[list] = None,
        tags: Optional[dict] = None,
    ) -> Optional[str]:
        """
        Complete experiment logging in a single call.
        Logs params, metrics, model, features, and dataset info.
        Returns run_id.
        """
        start_time = time.time()

        run_tags = {"model_type": model_name}
        if tags:
            run_tags.update(tags)

        run_id = self.start_run(run_name=model_name, tags=run_tags)

        try:
            self.log_params(params)
            self.log_metrics(metrics)
            self.log_dataset_info(X_train, X_test, y_train)
            self.log_feature_importance(model, feature_names)

            if confusion_matrix:
                self.log_confusion_matrix(confusion_matrix)

            # Log model with input example
            input_example = X_test.head(3)
            self.log_model(model, model_name, input_example)

            # Log training duration
            duration = round(time.time() - start_time, 2)
            self.log_metrics({"training_duration_sec": duration})

            logger.info(f"Experiment '{model_name}' logged (duration: {duration}s)")

        finally:
            self.end_run()

        return run_id

    def get_experiment_history(self, experiment_name: Optional[str] = None) -> pd.DataFrame:
        """Get all runs for an experiment as DataFrame."""
        if not self.is_available:
            return pd.DataFrame()

        exp_name = experiment_name or self.setup.experiment_name
        experiment = self.setup.mlflow.get_experiment_by_name(exp_name)
        if experiment is None:
            return pd.DataFrame()

        runs = self.setup.mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
        )
        return runs
