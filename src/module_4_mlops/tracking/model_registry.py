"""
Model Registry

Manages model versioning and stage transitions:
- Register trained models with versioning
- Promote models through stages (Staging → Production → Archived)
- Load production models for inference
- Track model lineage and metadata
"""

import logging
import joblib
from pathlib import Path
from typing import Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
MODELS_DIR = ROOT_DIR / "models"

# Valid stage transitions
VALID_STAGES = ["None", "Staging", "Production", "Archived"]


class ModelRegistry:
    """Manages model registration, versioning, and deployment stages."""

    def __init__(self, mlflow_setup=None):
        self.setup = mlflow_setup
        self.mlflow = None
        self.client = None
        self._init_registry()

    def _init_registry(self):
        """Initialize MLflow model registry client."""
        if self.setup and self.setup.is_available:
            self.mlflow = self.setup.mlflow
            try:
                self.client = self.mlflow.tracking.MlflowClient()
                logger.info("Model registry initialized")
            except Exception as e:
                logger.warning(f"Registry init failed: {e}")

    @property
    def is_available(self) -> bool:
        return self.client is not None

    def register_model(
        self,
        run_id: str,
        model_name: str,
        artifact_path: Optional[str] = None,
        tags: Optional[dict] = None,
    ) -> Optional[dict]:
        """Register a model from an MLflow run."""
        if not self.is_available:
            logger.warning("Registry unavailable. Skipping registration.")
            return None

        art_path = artifact_path or model_name
        model_uri = f"runs:/{run_id}/{art_path}"

        try:
            result = self.mlflow.register_model(model_uri, model_name)
            version = result.version

            # Add tags
            if tags:
                for key, value in tags.items():
                    self.client.set_model_version_tag(model_name, version, key, str(value))

            logger.info(f"Registered '{model_name}' v{version}")
            return {
                "name": model_name,
                "version": version,
                "source": model_uri,
                "status": result.status,
            }
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return None

    def transition_stage(
        self,
        model_name: str,
        version: str,
        stage: str,
        archive_existing: bool = True,
    ) -> Optional[dict]:
        """Transition a model version to a new stage."""
        if not self.is_available:
            return None

        if stage not in VALID_STAGES:
            logger.error(f"Invalid stage '{stage}'. Must be one of: {VALID_STAGES}")
            return None

        try:
            result = self.client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage=stage,
                archive_existing_versions=archive_existing,
            )
            logger.info(f"'{model_name}' v{version} → {stage}")
            return {
                "name": model_name,
                "version": result.version,
                "stage": result.current_stage,
            }
        except Exception as e:
            logger.error(f"Stage transition failed: {e}")
            return None

    def get_production_model(self, model_name: str) -> Optional[Any]:
        """Load the production-stage model for inference."""
        if not self.is_available:
            return self._load_local_model(model_name)

        try:
            model_uri = f"models:/{model_name}/Production"
            model = self.mlflow.sklearn.load_model(model_uri)
            logger.info(f"Loaded production model: {model_name}")
            return model
        except Exception as e:
            logger.warning(f"Failed to load from registry: {e}")
            return self._load_local_model(model_name)

    def get_latest_version(self, model_name: str, stage: Optional[str] = None) -> Optional[dict]:
        """Get the latest version of a model, optionally filtered by stage."""
        if not self.is_available:
            return None

        try:
            versions = self.client.get_latest_versions(
                model_name,
                stages=[stage] if stage else None,
            )
            if not versions:
                return None

            latest = versions[0]
            return {
                "name": latest.name,
                "version": latest.version,
                "stage": latest.current_stage,
                "run_id": latest.run_id,
                "source": latest.source,
                "status": latest.status,
            }
        except Exception as e:
            logger.error(f"Version lookup failed: {e}")
            return None

    def list_models(self) -> list:
        """List all registered models."""
        if not self.is_available:
            return self._list_local_models()

        try:
            models = self.client.search_registered_models()
            return [
                {
                    "name": m.name,
                    "latest_versions": [
                        {"version": v.version, "stage": v.current_stage}
                        for v in m.latest_versions
                    ],
                    "description": m.description or "",
                }
                for m in models
            ]
        except Exception as e:
            logger.error(f"List models failed: {e}")
            return self._list_local_models()

    def compare_versions(self, model_name: str) -> list:
        """Compare all versions of a model with their metrics."""
        if not self.is_available:
            return []

        try:
            versions = self.client.search_model_versions(f"name='{model_name}'")
            comparisons = []

            for v in versions:
                run = self.client.get_run(v.run_id)
                comparisons.append({
                    "version": v.version,
                    "stage": v.current_stage,
                    "status": v.status,
                    "metrics": run.data.metrics,
                    "run_id": v.run_id,
                })

            return sorted(comparisons, key=lambda x: int(x["version"]), reverse=True)
        except Exception as e:
            logger.error(f"Version comparison failed: {e}")
            return []

    def _load_local_model(self, model_name: str) -> Optional[Any]:
        """Fallback: load model from local disk."""
        paths = [
            MODELS_DIR / "cancellation" / "best_model.joblib",
            MODELS_DIR / "cancellation" / f"{model_name.lower().replace(' ', '_')}.joblib",
            MODELS_DIR / f"{model_name}.joblib",
        ]
        for path in paths:
            if path.exists():
                model = joblib.load(path)
                logger.info(f"Loaded local model: {path}")
                return model

        logger.warning(f"No local model found for '{model_name}'")
        return None

    def _list_local_models(self) -> list:
        """List locally saved models."""
        models = []
        for model_dir in MODELS_DIR.glob("*"):
            if model_dir.is_dir():
                joblib_files = list(model_dir.glob("*.joblib"))
                if joblib_files:
                    models.append({
                        "name": model_dir.name,
                        "files": [f.name for f in joblib_files],
                        "source": "local",
                    })
        return models

    def get_status(self) -> dict:
        """Get registry status."""
        return {
            "registry_available": self.is_available,
            "registered_models": len(self.list_models()),
            "models": self.list_models(),
        }
