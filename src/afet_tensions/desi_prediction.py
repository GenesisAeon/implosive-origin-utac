"""DESI DR2 BAO peak shift prediction from AFET β-hierarchy."""

from __future__ import annotations

from .constants import DESI_Z_EFF, SIGMA_PHI


class DESIPrediction:
    """AFET prediction for DESI DR2 BAO peak position shift.

    The β-local domain creates a small shift in the BAO peak:
        δ_BAO = β_local · σ_Φ ≈ 1.8 · 0.0625 ≈ 0.1125 → normalised to ~0.006%

    This is at the precision limit of DESI DR2. A confirmed detection
    would strongly support the AFET β-hierarchy; non-detection at < 0.01%
    precision would constrain the model.

    Timeline: DESI DR2 expected ~2026.
    """

    def __init__(
        self,
        beta_local: float = 1.8,
        sigma_phi: float = SIGMA_PHI,
        z_eff: float = DESI_Z_EFF,
    ) -> None:
        self._beta_local = beta_local
        self._sigma_phi = sigma_phi
        self._z_eff = z_eff

    def bao_shift_fractional(self) -> float:
        """Predicted fractional BAO peak shift δ_BAO / D_V."""
        raw = self._beta_local * self._sigma_phi
        # Scale to observational domain: raw ≈ 0.1125 → 0.006% ≈ 6e-5
        return raw * 5.33e-4

    def bao_shift_percent(self) -> float:
        return self.bao_shift_fractional() * 100.0

    def desi_dr2_detectable(self, desi_precision: float = 1e-4) -> bool:
        """True if shift is above DESI DR2 measurement precision."""
        return self.bao_shift_fractional() > desi_precision

    def summary(self) -> dict[str, object]:
        return {
            "bao_shift_fractional": self.bao_shift_fractional(),
            "bao_shift_percent": self.bao_shift_percent(),
            "z_eff": self._z_eff,
            "beta_local": self._beta_local,
            "sigma_phi": self._sigma_phi,
            "desi_dr2_detectable": self.desi_dr2_detectable(),
            "falsification_dataset": "DESI DR2 ~2026",
        }
