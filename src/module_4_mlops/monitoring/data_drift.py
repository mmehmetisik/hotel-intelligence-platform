"""
Data Drift Monitor

Detects distribution changes in input features between training
and production data using statistical tests:
- Population Stability Index (PSI)
- Kolmogorov-Smirnov (KS) test
- Feature-level drift reports with severity classification
"""

import numpy as np
import pandas as pd
import logging
from typing import Optional
from scipy import stats
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DriftResult:
    """Result of a drift detection analysis."""
    feature: str
    psi: float
    ks_statistic: float
    ks_pvalue: float
    drift_detected: bool
    severity: str  # "none", "warning", "critical"
    reference_mean: float = 0.0
    current_mean: float = 0.0
    mean_shift_pct: float = 0.0


@dataclass
class DriftReport:
    """Complete drift analysis report."""
    timestamp: str = ""
    total_features: int = 0
    drifted_features: int = 0
    drift_ratio: float = 0.0
    overall_severity: str = "none"
    feature_results: list = field(default_factory=list)
    summary: str = ""


class DataDriftMonitor:
    """Monitors feature distribution drift between reference and current data."""

    # PSI thresholds
    PSI_WARNING = 0.1
    PSI_CRITICAL = 0.2

    # KS test significance level
    KS_ALPHA = 0.05

    def __init__(self, reference_data: Optional[pd.DataFrame] = None):
        self.reference_data = reference_data
        self.drift_history = []

    def set_reference(self, data: pd.DataFrame):
        """Set the reference (training) data distribution."""
        self.reference_data = data.select_dtypes(include="number").copy()
        logger.info(f"Reference data set: {self.reference_data.shape}")

    def calculate_psi(self, reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
        """
        Calculate Population Stability Index (PSI).

        PSI < 0.1  → No significant change
        PSI 0.1-0.2 → Moderate change (warning)
        PSI > 0.2  → Significant change (action needed)
        """
        # Create bins from reference distribution
        min_val = min(reference.min(), current.min())
        max_val = max(reference.max(), current.max())

        if min_val == max_val:
            return 0.0

        bin_edges = np.linspace(min_val, max_val, bins + 1)

        ref_counts = np.histogram(reference, bins=bin_edges)[0]
        cur_counts = np.histogram(current, bins=bin_edges)[0]

        # Add small epsilon to avoid division by zero / log(0)
        eps = 1e-6
        ref_pct = (ref_counts + eps) / (ref_counts.sum() + eps * bins)
        cur_pct = (cur_counts + eps) / (cur_counts.sum() + eps * bins)

        psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
        return float(psi)

    def check_feature_drift(self, feature_name: str, current_values: np.ndarray) -> DriftResult:
        """Check drift for a single feature."""
        if self.reference_data is None or feature_name not in self.reference_data.columns:
            return DriftResult(
                feature=feature_name, psi=0.0,
                ks_statistic=0.0, ks_pvalue=1.0,
                drift_detected=False, severity="none",
            )

        ref_values = self.reference_data[feature_name].dropna().values
        cur_values = pd.Series(current_values).dropna().values

        if len(ref_values) == 0 or len(cur_values) == 0:
            return DriftResult(
                feature=feature_name, psi=0.0,
                ks_statistic=0.0, ks_pvalue=1.0,
                drift_detected=False, severity="none",
            )

        # PSI
        psi = self.calculate_psi(ref_values, cur_values)

        # KS test
        ks_stat, ks_pvalue = stats.ks_2samp(ref_values, cur_values)

        # Determine severity
        drift_detected = psi >= self.PSI_WARNING or ks_pvalue < self.KS_ALPHA
        if psi >= self.PSI_CRITICAL:
            severity = "critical"
        elif psi >= self.PSI_WARNING:
            severity = "warning"
        else:
            severity = "none"

        # Mean shift
        ref_mean = float(np.mean(ref_values))
        cur_mean = float(np.mean(cur_values))
        mean_shift = abs(cur_mean - ref_mean) / (abs(ref_mean) + 1e-10) * 100

        return DriftResult(
            feature=feature_name,
            psi=round(psi, 4),
            ks_statistic=round(float(ks_stat), 4),
            ks_pvalue=round(float(ks_pvalue), 4),
            drift_detected=drift_detected,
            severity=severity,
            reference_mean=round(ref_mean, 4),
            current_mean=round(cur_mean, 4),
            mean_shift_pct=round(mean_shift, 2),
        )

    def analyze(self, current_data: pd.DataFrame, features: Optional[list] = None) -> DriftReport:
        """Run full drift analysis on current data vs reference."""
        if self.reference_data is None:
            logger.error("No reference data set. Call set_reference() first.")
            return DriftReport(summary="No reference data available.")

        current_numeric = current_data.select_dtypes(include="number")

        if features:
            cols = [c for c in features if c in current_numeric.columns and c in self.reference_data.columns]
        else:
            cols = [c for c in current_numeric.columns if c in self.reference_data.columns]

        results = []
        for col in cols:
            result = self.check_feature_drift(col, current_numeric[col].values)
            results.append(result)

        drifted = [r for r in results if r.drift_detected]
        critical = [r for r in results if r.severity == "critical"]

        # Overall severity
        if len(critical) > 0:
            overall = "critical"
        elif len(drifted) > len(results) * 0.3:
            overall = "warning"
        elif len(drifted) > 0:
            overall = "minor"
        else:
            overall = "none"

        drift_ratio = len(drifted) / max(len(results), 1)

        # Summary text
        summary = (
            f"Analyzed {len(results)} features: "
            f"{len(drifted)} drifted ({drift_ratio:.0%}), "
            f"{len(critical)} critical. "
            f"Overall severity: {overall}."
        )

        report = DriftReport(
            timestamp=pd.Timestamp.now().isoformat(),
            total_features=len(results),
            drifted_features=len(drifted),
            drift_ratio=round(drift_ratio, 4),
            overall_severity=overall,
            feature_results=results,
            summary=summary,
        )

        self.drift_history.append(report)
        logger.info(summary)
        return report

    def get_drift_summary_df(self, report: DriftReport) -> pd.DataFrame:
        """Convert drift report to a pandas DataFrame for display."""
        if not report.feature_results:
            return pd.DataFrame()

        return pd.DataFrame([
            {
                "Feature": r.feature,
                "PSI": r.psi,
                "KS Stat": r.ks_statistic,
                "KS p-value": r.ks_pvalue,
                "Drift": "Yes" if r.drift_detected else "No",
                "Severity": r.severity,
                "Ref Mean": r.reference_mean,
                "Cur Mean": r.current_mean,
                "Mean Shift %": r.mean_shift_pct,
            }
            for r in report.feature_results
        ]).sort_values("PSI", ascending=False)
