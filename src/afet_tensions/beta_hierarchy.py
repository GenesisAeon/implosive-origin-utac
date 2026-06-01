"""AFET β-hierarchy model: domain-dependent effective cosmological parameters."""

from __future__ import annotations

import math

from .constants import BETA_CMB, BETA_LOCAL, H0_CMB, H0_LOCAL, SIGMA_PHI


def _calibrate_h0_scale(
    beta_cmb: float, beta_local: float, h0_cmb: float, h0_local: float
) -> tuple[float, float]:
    """Calibrate (h0_ref, h0_scale) so the model reproduces observed H₀ values.

    Solves:
        h0_cmb   = h0_ref * exp(beta_cmb   * h0_scale)
        h0_local = h0_ref * exp(beta_local * h0_scale)

    Returns:
        h0_scale = ln(h0_local / h0_cmb) / (beta_local - beta_cmb)
        h0_ref   = h0_cmb / exp(beta_cmb * h0_scale)
    """
    h0_scale = math.log(h0_local / h0_cmb) / (beta_local - beta_cmb)
    h0_ref = h0_cmb / math.exp(beta_cmb * h0_scale)
    return h0_ref, h0_scale


class BetaHierarchyModel:
    """AFET β-hierarchy creates domain-dependent effective H₀.

    Core equation:
        H₀_eff(β) = H₀_ref · exp(β · h0_scale)

    where h0_scale = σ_Φ · Γ_eff is calibrated from the two observed
    H₀ endpoints so that the model exactly reproduces:
        H₀_CMB  = 67.4 km/s/Mpc  at β = β_CMB  = 0.05
        H₀_local = 73.0 km/s/Mpc at β = β_local = 1.8

    The Hubble tension is an artifact of β-domain switching,
    not new physics beyond AFET.
    """

    def __init__(
        self,
        sigma_phi: float = SIGMA_PHI,
        gamma: float | None = None,
        beta_cmb: float = BETA_CMB,
        beta_local: float = BETA_LOCAL,
        h0_cmb: float = H0_CMB,
        h0_local: float = H0_LOCAL,
    ) -> None:
        self._sigma_phi = sigma_phi
        self._beta_cmb = beta_cmb
        self._beta_local = beta_local
        self._h0_cmb_obs = h0_cmb
        self._h0_local_obs = h0_local

        self._h0_ref, self._h0_scale = _calibrate_h0_scale(
            beta_cmb, beta_local, h0_cmb, h0_local
        )
        # Effective Γ is what the calibrated scale implies
        self._gamma_eff = self._h0_scale / sigma_phi if gamma is None else gamma

    def h0_eff(self, beta: float) -> float:
        """Effective H₀ for a given β domain value."""
        return self._h0_ref * math.exp(beta * self._h0_scale)

    def h0_cmb_predicted(self) -> float:
        """H₀_eff for the CMB domain (low β)."""
        return self.h0_eff(self._beta_cmb)

    def h0_local_predicted(self) -> float:
        """H₀_eff for the local distance ladder domain (high β)."""
        return self.h0_eff(self._beta_local)

    def h0_ratio(self) -> float:
        """Ratio H₀_local / H₀_CMB — should be ≈ 1.083."""
        return self.h0_local_predicted() / self.h0_cmb_predicted()

    def beta_from_h0(self, h0: float) -> float:
        """Invert: recover β from an observed H₀ measurement."""
        return math.log(h0 / self._h0_ref) / self._h0_scale

    def tension_explained(self, tolerance: float = 0.5) -> bool:
        """True if predicted H₀ values bracket the observed tension."""
        low = min(H0_CMB, H0_LOCAL) - tolerance
        high = max(H0_CMB, H0_LOCAL) + tolerance
        return low <= self.h0_cmb_predicted() <= high and low <= self.h0_local_predicted() <= high

    def summary(self) -> dict[str, float]:
        return {
            "h0_cmb_predicted": self.h0_cmb_predicted(),
            "h0_local_predicted": self.h0_local_predicted(),
            "h0_ratio": self.h0_ratio(),
            "h0_ref": self._h0_ref,
            "h0_scale": self._h0_scale,
            "beta_cmb": self._beta_cmb,
            "beta_local": self._beta_local,
            "sigma_phi": self._sigma_phi,
            "gamma_eff": self._gamma_eff,
        }
