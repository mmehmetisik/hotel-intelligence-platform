"""
MLOps Training Pipeline

Wraps the existing model training with MLflow experiment tracking.
Provides a production-ready pipeline that:
1. Loads and prepares data
2. Trains models with experiment logging
3. Registers the best model
4. Sets up monitoring baselines
"""

import logging
import json
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.module_4_mlops.tracking.mlflow_setup import MLflowSetup
from src.module_4_mlops.tracking.experiment_logger import ExperimentLogger
from src.module_4_mlops.tracking.model_registry import ModelRegistry
from src.module_4_mlops.monitoring.data_drift import DataDriftMonitor
from src.module_4_mlops.monitoring.model_drift import ModelDriftMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models" / "cancellation"
RANDOM_SEED = 42


class TrainingPipeline:
    """
    Production training pipeline with full MLOps integration.
    Wraps model training with experiment tracking, registration,
    and monitoring baseline setup.
    """

    def __init__(self, experiment_name: str = "hotel-cancellation"):
        self.experiment_name = experiment_name
        self.setup = MLflowSetup(experiment_name=experiment_name)
        self.exp_logger = ExperimentLogger(self.setup)
        self.registry = ModelRegistry(self.setup)
        self.data_drift_monitor = DataDriftMonitor()
        self.model_drift_monitor = ModelDriftMonitor()

    def run(
        self,
        df: pd.DataFrame,
        feature_cols: list,
        target_col: str = "is_canceled",
        test_size: float = 0.2,
        register_best: bool = True,
    ) -> dict:
        """
        Execute the full training pipeline with MLOps tracking.

        Returns dict with results, best model, and monitoring baselines.
        """
        logger.info("=" * 60)
        logger.info("  MLOPS TRAINING PIPELINE")
        logger.info("=" * 60)

        # Step 1: Prepare data
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=RANDOM_SEED, stratify=y
        )

        logger.info(f"Data: {X_train.shape[0]} train, {X_test.shape[0]} test, {len(feature_cols)} features")

        # Step 2: Train models with logging
        from src.module_1_predictive.cancellation.train import get_models, evaluate_model
        from sklearn.preprocessing import StandardScaler

        models = get_models()
        scaler = StandardScaler()
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
        )
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test), columns=X_test.columns, index=X_test.index
        )

        all_results = {}
        run_ids = {}

        for name, model in models.items():
            logger.info(f"\nTraining {name}...")

            if name == "Logistic Regression":
                model.fit(X_train_scaled, y_train)
                metrics = evaluate_model(model, X_test_scaled, y_test, name)
            else:
                model.fit(X_train, y_train)
                metrics = evaluate_model(model, X_test, y_test, name)

            # Extract params
            params = {k: str(v) for k, v in model.get_params().items()
                      if not callable(v) and v is not None}

            # Log to MLflow
            run_id = self.exp_logger.log_training_run(
                model=model,
                model_name=name.lower().replace(" ", "_"),
                params=params,
                metrics={k: v for k, v in metrics.items()
                         if isinstance(v, (int, float))},
                X_train=X_train if name != "Logistic Regression" else X_train_scaled,
                X_test=X_test if name != "Logistic Regression" else X_test_scaled,
                y_train=y_train,
                feature_names=feature_cols,
                confusion_matrix=metrics.get("confusion_matrix"),
                tags={"pipeline": "cancellation", "phase": "training"},
            )

            all_results[name] = metrics
            run_ids[name] = run_id

        # Step 3: Select best model
        best_name = max(all_results, key=lambda k: all_results[k]["auc_roc"])
        best_model = models[best_name]
        best_metrics = all_results[best_name]
        logger.info(f"\nBest: {best_name} (AUC: {best_metrics['auc_roc']})")

        # Step 4: Register best model
        if register_best and run_ids.get(best_name):
            self.registry.register_model(
                run_id=run_ids[best_name],
                model_name="cancellation_predictor",
                artifact_path=best_name.lower().replace(" ", "_"),
                tags={"auc_roc": str(best_metrics["auc_roc"])},
            )

        # Step 5: Set monitoring baselines
        self.data_drift_monitor.set_reference(X_train)

        if best_name == "Logistic Regression":
            y_proba = best_model.predict_proba(X_test_scaled)[:, 1]
        else:
            y_proba = best_model.predict_proba(X_test)[:, 1]

        self.model_drift_monitor.set_baseline(y_test.values, y_proba)

        logger.info("\n" + "=" * 60)
        logger.info("  PIPELINE COMPLETE")
        logger.info("=" * 60)

        return {
            "results": all_results,
            "best_model_name": best_name,
            "best_metrics": best_metrics,
            "run_ids": run_ids,
            "data_drift_monitor": self.data_drift_monitor,
            "model_drift_monitor": self.model_drift_monitor,
        }

    def load_saved_baseline(self) -> Optional[dict]:
        """Load baseline metrics from saved model metadata."""
        metadata_path = MODELS_DIR / "metadata.json"
        if not metadata_path.exists():
            return None

        with open(metadata_path) as f:
            metadata = json.load(f)

        results_path = MODELS_DIR / "model_comparison.csv"
        if results_path.exists():
            results = pd.read_csv(results_path, index_col=0)
            best_name = metadata.get("best_model")
            if best_name and best_name in results.index:
                row = results.loc[best_name]
                return {
                    "model_name": best_name,
                    "auc_roc": row.get("auc_roc", 0),
                    "f1": row.get("f1", 0),
                    "precision": row.get("precision", 0),
                    "recall": row.get("recall", 0),
                    "accuracy": row.get("accuracy", 0),
                }

        return metadata

    def get_status(self) -> dict:
        """Get pipeline status."""
        return {
            "mlflow": self.setup.get_status(),
            "registry": self.registry.get_status(),
            "baseline_loaded": self.model_drift_monitor.baseline_metrics is not None,
        }
