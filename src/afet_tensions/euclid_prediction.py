"""Euclid DR1 weak-lensing prediction from AFET S₈ redshift dependence."""

from __future__ import annotations

from .constants import S8_CMB
from .crep_redshift import CREPRedshiftEvolution


class EuclidPrediction:
    """AFET prediction for Euclid DR1 weak-lensing S₈(z).

    AFET predicts S₈(z) = S₈_CMB · (1 - 0.05·z) for z < 1.5,
    driven by CREP-damped structure growth.

    If Euclid DR1 measures a slope steeper or shallower by > 2σ,
    the CREP redshift evolution model is falsified.

    Timeline: Euclid DR1 expected ~2026-2027.
    """

    def __init__(
        self,
        crep: CREPRedshiftEvolution | None = None,
        linear_slope: float = -0.05,
    ) -> None:
        self._crep = crep or CREPRedshiftEvolution()
        self._linear_slope = linear_slope

    def s8_linear_prediction(self, z: float) -> float:
        """Simple linear approximation: S₈_CMB · (1 - 0.05·z)."""
        return S8_CMB * (1.0 + self._linear_slope * z)

    def s8_full_prediction(self, z: float) -> float:
        """Full CREP-model prediction."""
        return self._crep.s8_at_z(z)

    def z_grid(self, z_max: float = 1.5, n: int = 10) -> list[float]:
        dz = z_max / (n - 1)
        return [i * dz for i in range(n)]

    def euclid_survey_predictions(self) -> list[dict[str, float]]:
        """S₈ predictions at Euclid survey redshifts."""
        return [
            {
                "z": z,
                "s8_linear": self.s8_linear_prediction(z),
                "s8_crep": self.s8_full_prediction(z),
            }
            for z in self.z_grid()
        ]

    def summary(self) -> dict[str, object]:
        return {
            "linear_slope_per_z": self._linear_slope,
            "s8_z0_linear": self.s8_linear_prediction(0.0),
            "s8_z09_linear": self.s8_linear_prediction(0.9),
            "s8_z15_linear": self.s8_linear_prediction(1.5),
            "s8_z09_crep": self.s8_full_prediction(0.9),
            "survey_predictions": self.euclid_survey_predictions(),
            "falsification_dataset": "Euclid DR1 ~2027",
        }
