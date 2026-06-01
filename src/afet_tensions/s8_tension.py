"""AFET explanation for the S₈ tension via CREP-damped structure growth."""

from __future__ import annotations

from .constants import S8_CMB, S8_WEAK_LENSING
from .crep_redshift import CREPRedshiftEvolution


class S8Tension:
    """CREP-damped structure growth as explanation for S₈ tension.

    S₈_CMB ≈ 0.832 (Planck 2018) vs S₈_WL ≈ 0.759 (KiDS-1000 + DES Y3).

    AFET prediction:
        S₈(z) = S₈_CMB · tanh(σ · Γ(z)) / tanh(σ · Γ_CMB)

    At low redshift, Γ(z) decreases → S₈ decreases.
    The weak-lensing surveys probe z ≲ 1, where CREP damping is active.

    Falsification: Euclid DR1 should measure S₈(z) following the
    predicted linear decline S₈(z) ≈ S₈_CMB · (1 - 0.05·z) for z < 1.5.
    """

    def __init__(self, crep: CREPRedshiftEvolution | None = None) -> None:
        self._crep = crep or CREPRedshiftEvolution()

    def s8_predicted(self, z: float) -> float:
        """Predicted S₈ at redshift z."""
        return self._crep.s8_at_z(z)

    def s8_z0_predicted(self) -> float:
        """Predicted S₈ at z=0 (weak lensing limit)."""
        return self._crep.s8_at_z(0.0)

    def s8_cmb_predicted(self) -> float:
        """Predicted S₈ at z_CMB (should recover S8_CMB)."""
        return self._crep.s8_at_z(1100.0)

    def tension_resolved(self, tolerance: float = 0.02) -> bool:
        """True if predicted S₈(z=0) agrees with observed weak lensing within tolerance."""
        return abs(self.s8_z0_predicted() - S8_WEAK_LENSING) < tolerance

    def euclid_slope_prediction(self) -> float:
        """dS₈/dz slope for Euclid DR1 validation [per unit redshift]."""
        return self._crep.s8_slope()

    def summary(self) -> dict[str, float | bool]:
        return {
            "s8_cmb_observed": S8_CMB,
            "s8_wl_observed": S8_WEAK_LENSING,
            "s8_z0_predicted": self.s8_z0_predicted(),
            "s8_z1_predicted": self.s8_predicted(1.0),
            "s8_cmb_predicted": self.s8_cmb_predicted(),
            "tension_resolved_2pct": self.tension_resolved(),
            "euclid_slope_per_z": self.euclid_slope_prediction(),
        }
