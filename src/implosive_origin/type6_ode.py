"""UTAC Type-6: Implosive / reversed dynamics ODE."""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Type6ODEParams:
    """Parameters for the Type-6 reversed UTAC ODE."""

    r: float = 1.0       # growth rate (positive; reversed sign in ODE)
    K_min: float = 0.01  # minimum carrying capacity (inflationary fixed point)
    sigma: float = 0.0625  # σ_Φ = 1/16 (Frame Principle)
    gamma: float = 0.309   # CREP Γ coupling (≈ golden-ratio derived)


@dataclass
class Type6State:
    """State along a Type-6 ODE trajectory."""

    t: float
    H: float
    dHdt: float
    at_fixed_point: bool = False


class Type6ODE:
    """UTAC Type-6: reversed logistic dynamics modelling pre-inflationary collapse.

    Standard UTAC:  dH/dt =  r·H·(1 - H/K)·tanh(σΓ)   [expansion]
    Type-6 reversal: dH/dt = -r·H·(1 - H/K_min)·tanh(σΓ)  [implosive collapse]

    H decreases from H_max (pre-inflationary maximum) toward H_min
    (inflationary fixed point = observable universe onset).

    The Phase Transition at H* = K_min · tanh(σΓ) is the
    "ignition" of standard inflation — the matter-creation event.
    """

    def __init__(self, params: Type6ODEParams | None = None) -> None:
        self.p = params or Type6ODEParams()
        self._trajectory: list[Type6State] = []

    # ------------------------------------------------------------------
    # Core physics
    # ------------------------------------------------------------------

    def dHdt(self, H: float) -> float:
        """Compute dH/dt for the Type-6 reversed ODE.

        Implosive form: dH/dt = -r·H·(1 - K_min/H)·tanh(σΓ)
        Fixed point at H = K_min. For H > K_min: dH/dt < 0 (collapsing).
        """
        if H <= 0:
            return 0.0
        activation = math.tanh(self.p.sigma * self.p.gamma)
        return -self.p.r * H * (1.0 - self.p.K_min / H) * activation

    def fixed_point(self) -> float:
        """Return H* = K_min · tanh(σΓ) — the inflationary ignition point."""
        return self.p.K_min * math.tanh(self.p.sigma * self.p.gamma)

    # ------------------------------------------------------------------
    # Integration (simple Euler with adaptive step)
    # ------------------------------------------------------------------

    def integrate(
        self,
        H0: float = 1.0,
        t_max: float = 60.0,
        n_steps: int = 6000,
    ) -> list[Type6State]:
        """Integrate the Type-6 ODE from H0 down toward H*."""
        dt = t_max / n_steps
        H = H0
        H_star = self.fixed_point()
        states: list[Type6State] = []

        for i in range(n_steps + 1):
            t = i * dt
            dhdt = self.dHdt(H)
            at_fp = abs(H - H_star) < 1e-4 * H_star if H_star > 0 else False
            states.append(Type6State(t=t, H=H, dHdt=dhdt, at_fixed_point=at_fp))
            if at_fp:
                break
            H = max(H_star, H + dhdt * dt)  # clamp to fixed point

        self._trajectory = states
        return states

    @property
    def trajectory(self) -> list[Type6State]:
        return self._trajectory

    def efolds(self, H0: float = 1.0) -> float:
        """Estimate e-folds from H0 to H*: N ≈ ln(H0 / H*)."""
        H_star = self.fixed_point()
        if H_star <= 0:
            return float("nan")
        return math.log(H0 / H_star)
