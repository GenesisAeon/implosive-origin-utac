"""AFET explanation for the Hubble tension via β-hierarchy."""

from __future__ import annotations

from .beta_hierarchy import BetaHierarchyModel
from .constants import H0_CMB, H0_LOCAL


class HubbleTension:
    """AFET β-hierarchy explanation for the H₀ tension.

    The tension H₀_local ≈ 73.0 vs H₀_CMB ≈ 67.4 km/s/Mpc arises
    because different probes sample different β-domains.

    Late-universe probes (SNe Ia, Cepheids): high β → high H₀_eff.
    Early-universe probes (CMB, BAO): low β → low H₀_eff.

    This module quantifies the β-domain switching and tests whether
    the observed ratio 73.0/67.4 ≈ 1.083 is reproduced.
    """

    def __init__(self, model: BetaHierarchyModel | None = None) -> None:
        self._model = model or BetaHierarchyModel()

    def observed_ratio(self) -> float:
        return H0_LOCAL / H0_CMB

    def predicted_ratio(self) -> float:
        return self._model.h0_ratio()

    def ratio_agreement(self, tolerance: float = 0.01) -> bool:
        return abs(self.predicted_ratio() - self.observed_ratio()) < tolerance

    def tension_sigma(self) -> float:
        """Tension in σ units between local and CMB H₀ (simplified)."""
        combined_uncertainty = (0.5**2 + 0.3**2) ** 0.5
        return abs(H0_LOCAL - H0_CMB) / combined_uncertainty

    def afet_resolves_tension(self, sigma_threshold: float = 2.0) -> bool:
        """True if AFET β-hierarchy reduces tension below sigma_threshold.

        After β-correction, the residual tension between predicted CMB
        and local values should be < sigma_threshold σ.
        """
        delta = abs(self._model.h0_local_predicted() - self._model.h0_cmb_predicted())
        combined_uncertainty = (0.5**2 + 0.3**2) ** 0.5
        residual_sigma = delta / combined_uncertainty
        return residual_sigma < sigma_threshold

    def summary(self) -> dict[str, float | bool]:
        return {
            "h0_local_observed": H0_LOCAL,
            "h0_cmb_observed": H0_CMB,
            "h0_local_predicted": self._model.h0_local_predicted(),
            "h0_cmb_predicted": self._model.h0_cmb_predicted(),
            "observed_ratio": self.observed_ratio(),
            "predicted_ratio": self.predicted_ratio(),
            "tension_sigma": self.tension_sigma(),
            "ratio_agreement_1pct": self.ratio_agreement(),
            "afet_resolves_tension": self.afet_resolves_tension(),
        }
