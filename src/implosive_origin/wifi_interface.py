"""Interface to the WIFI model (Freese et al. 2023, arXiv:2309.14412).

SPECULATIVE: This module provides a conceptual bridge between the WIFI
(Wave-function of Inflation / pre-inflationary dark matter) model and
the UTAC Type-6 dynamics. It does NOT reproduce the full WIFI calculation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .constants import PHI, SIGMA_PHI, V_RIG_KM_S


@dataclass
class WIFIParams:
    """WIFI model parameters mapped to UTAC Type-6."""

    lambda_dm: float = 1e-3   # dark matter self-coupling
    phi_0: float = PHI        # initial field value (Φ by convention)
    sigma_phi: float = SIGMA_PHI


class WIFIInterface:
    """Conceptual interface between WIFI pre-inflation dark matter and UTAC Type-6.

    WIFI model (Freese et al.): dark matter density ρ_DM evolves during
    pre-inflationary phase. In UTAC terms this is a Type-6 implosive process.

    Mapping (approximate):
        ρ_DM(t) ↔ H(t) in Type-6 ODE
        WIFI inflation onset ↔ UTAC Type-6 phase transition H → H*
        WIFI λ_DM coupling ↔ UTAC σ parameter
    """

    def __init__(self, params: WIFIParams | None = None) -> None:
        self.params = params or WIFIParams()

    def utac_sigma_from_lambda(self) -> float:
        """Map WIFI coupling λ_DM to UTAC σ.

        Heuristic: σ_UTAC ≈ σ_Φ · (1 + log(1/λ_DM))
        """
        import math

        return self.params.sigma_phi * (1.0 + math.log(1.0 / max(self.params.lambda_dm, 1e-10)))

    def dm_density_utac(self, H: float, H_max: float = 1.0) -> float:
        """Normalised dark matter density as fraction of pre-inflationary max."""
        return H / H_max if H_max > 0 else 0.0

    def inflation_onset_condition(self, H: float, H_star: float) -> bool:
        """True when Type-6 system has reached the inflation onset threshold."""
        return H_star * 1.01 >= H  # within 1% of fixed point

    def reference(self) -> str:
        return "Freese et al. (2023), arXiv:2309.14412 — WIFI Model"

    def summary(self) -> dict[str, object]:
        return {
            "reference": self.reference(),
            "lambda_dm": self.params.lambda_dm,
            "utac_sigma": self.utac_sigma_from_lambda(),
            "v_rig_km_s": V_RIG_KM_S,
            "status": "SPECULATIVE — conceptual mapping only",
        }
