"""Pre-inflationary entropy in UTAC Type-6 framework."""

from __future__ import annotations

import math

from .constants import PHI, SIGMA_PHI


class EntropyOrigin:
    """Pre-inflationary entropy S_pre ∝ K · ln(K).

    Analogue of de Sitter entropy: S_dS = π M_P² / H².
    In UTAC terms: S_pre(K) = K · ln(K) where K = carrying capacity.

    Physical interpretation:
        High K → high pre-inflationary entropy (many accessible states)
        Low K  → low entropy (ordered, inflaton-dominated)
        The phase transition K → K_min corresponds to entropy decrease.
    """

    def __init__(self, K_max: float = 10.0, K_min: float = 0.01,
                 sigma: float = SIGMA_PHI) -> None:
        self.K_max = K_max
        self.K_min = K_min
        self.sigma = sigma

    def entropy(self, K: float) -> float:
        """S_pre(K) = K · |ln(K)|."""
        if K <= 0:
            return 0.0
        return K * abs(math.log(K))

    def entropy_ratio(self) -> float:
        """S_pre(K_max) / S_pre(K_min) — entropy reduction at phase transition."""
        s_max = self.entropy(self.K_max)
        s_min = self.entropy(self.K_min)
        if s_min == 0:
            return float("inf")
        return s_max / s_min

    def phi_entropy(self) -> float:
        """Entropy at K = Φ — golden ratio as natural pre-inflationary scale."""
        return self.entropy(PHI)

    def sigma_entropy_product(self) -> float:
        """σ_Φ · S_pre(K_max) — Frame Principle modulated entropy."""
        return self.sigma * self.entropy(self.K_max)

    def summary(self) -> dict[str, object]:
        return {
            "K_max": self.K_max,
            "K_min": self.K_min,
            "S_pre_Kmax": self.entropy(self.K_max),
            "S_pre_Kmin": self.entropy(self.K_min),
            "entropy_ratio": self.entropy_ratio(),
            "S_pre_phi": self.phi_entropy(),
            "sigma_phi": self.sigma,
            "sigma_times_S_pre": self.sigma_entropy_product(),
        }
