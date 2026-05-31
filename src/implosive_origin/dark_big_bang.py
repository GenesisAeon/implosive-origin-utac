"""Dark Big Bang scenario within UTAC Type-6 framework.

Reference: Niedermayer (2023) — Dark Big Bang hypothesis.
SPECULATIVE: This is a theoretical bridge, not established physics.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import PHI, SIGMA_PHI, K_RIG_MPC


@dataclass
class DarkBigBangState:
    """Characterises the three epochs of the Dark Big Bang scenario."""

    epoch: str           # 'pre-dark', 'threshold', 'post-threshold'
    H: float             # UTAC H value
    entropy: float       # S_pre ∝ K·ln(K) estimate
    is_observable: bool  # True only for post-threshold epoch


class DarkBigBang:
    """UTAC Type-6 interpretation of the Dark Big Bang.

    Epoch map:
        pre-dark   → Universe in high-entropy H_max state (Type-6 start)
        threshold  → Phase transition H → H* (matter-creation event)
        post-threshold → Observable universe (low-H UTAC fixed point)

    Observable universe = post-threshold H* fixed point.
    """

    def __init__(self, H_max: float = 1.0, K_min: float = 0.01,
                 sigma: float = SIGMA_PHI, gamma: float = 0.309) -> None:
        self.H_max = H_max
        self.K_min = K_min
        self.sigma = sigma
        self.gamma = gamma
        self._H_star = K_min * math.tanh(sigma * gamma)

    def H_star(self) -> float:
        """Inflationary fixed point = onset of observable universe."""
        return self._H_star

    def entropy_pre(self, K: float | None = None) -> float:
        """Pre-inflationary entropy estimate: S_pre ∝ K · |ln(K)|.

        Analogue of de Sitter entropy: S_dS ∝ M_P² / H².
        Uses absolute value of log so S_pre ≥ 0 for all K > 0.
        """
        K = K if K is not None else self.H_max
        if K <= 0:
            return 0.0
        return K * abs(math.log(K))

    def epoch(self, H: float) -> DarkBigBangState:
        """Classify current H into a Dark Big Bang epoch."""
        if H > self._H_star * 10:
            e = "pre-dark"
            obs = False
        elif H > self._H_star * 1.1:
            e = "threshold"
            obs = False
        else:
            e = "post-threshold"
            obs = True
        return DarkBigBangState(
            epoch=e,
            H=H,
            entropy=self.entropy_pre(H),
            is_observable=obs,
        )

    def de_sitter_entropy_ratio(self) -> float:
        """Ratio S_pre(H_max) / S_pre(H*) — entropy reduction at phase transition."""
        s_max = self.entropy_pre(self.H_max)
        s_star = self.entropy_pre(self._H_star)
        if s_star == 0:
            return float("inf")
        return s_max / s_star

    def summary(self) -> dict[str, object]:
        return {
            "H_max": self.H_max,
            "H_star": self._H_star,
            "efolds_estimate": math.log(self.H_max / self._H_star) if self._H_star > 0 else None,
            "entropy_pre_Hmax": self.entropy_pre(self.H_max),
            "entropy_ratio": self.de_sitter_entropy_ratio(),
            "k_rig_mpc_inv": K_RIG_MPC,
            "status": "SPECULATIVE — Dark Big Bang hypothesis",
        }
