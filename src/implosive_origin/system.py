"""ImplosiveOriginUTAC — Diamond interface for Package 33."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .cmb_predictions import CMBPredictions
from .constants import (
    GAMMA_INFLATION,
    K_RIG_MPC,
    N_EFOLDS_STANDARD,
    PACKAGE_REGISTRY_ID,
    SIGMA_PHI,
    ZENODO_DOI,
)
from .dark_big_bang import DarkBigBang
from .dm_power_spectrum import DMPowerSpectrum
from .entropy_origin import EntropyOrigin
from .inflation_bridge import InflationBridge
from .type6_ode import Type6ODE, Type6ODEParams
from .wifi_interface import WIFIInterface

TYPE6_TARGETS: dict[str, tuple[float, float | None]] = {
    "tensor_scalar_r": (0.004, 0.001),
    "inflation_efolds": (60.0, 5.0),
    "dm_k_suppression_mpc_inv": (0.30, 0.10),  # k_RIG = v_RIG·H₀/c ≈ 0.304 Mpc⁻¹
    "type6_fixed_point": (1.0, None),    # 1 = True (well-defined)
    "bicep_compatible": (1.0, None),      # 1 = True
}

PACKAGE_REGISTRY: dict[str, Any] = {
    "id": PACKAGE_REGISTRY_ID,
    "name": "implosive-origin-utac",
    "class": "ImplosiveOriginUTAC",
    "domain": "cosmology",
    "scale": "pre-inflationary",
    "zenodo": ZENODO_DOI,
    "status": "speculative",
}


@dataclass
class CREPState:
    """CREP tensor state for the implosive origin system."""

    C: float = 0.8    # context continuity (pre-inflationary coherence)
    R: float = 0.7    # reproducibility (ODE determinism)
    E: float = 0.5    # entropy (pre-inflationary = high entropy)
    P: float = 0.4    # productivity (speculative — lower weight)

    def gamma(self) -> float:
        return float((self.C * self.R * self.E * self.P) ** 0.25)


@dataclass
class UTACState:
    """UTAC ODE state for the implosive origin system."""

    H: float = 1.0
    r: float = 1.0
    K: float = 0.01
    sigma: float = SIGMA_PHI
    beta: float = 0.309   # Γ-coupling (domain β for cosmology)


class ImplosiveOriginUTAC:
    """UTAC Type-6 — Implosive Origin Fields (GenesisAeon Package 33).

    Diamond interface implementing run_cycle, get_crep_state, get_utac_state,
    get_phase_events, to_zenodo_record, tensor_to_scalar_r, dm_suppression_scale.

    STATUS: SPECULATIVE cosmological module. See DISCLAIMER.md.
    """

    def __init__(
        self,
        H_max: float = 1.0,
        K_min: float = 0.01,
        sigma: float = SIGMA_PHI,
        gamma: float = GAMMA_INFLATION,
    ) -> None:
        self._H_max = H_max
        self._K_min = K_min
        self._sigma = sigma
        self._gamma = gamma

        self._ode = Type6ODE(Type6ODEParams(r=1.0, K_min=K_min, sigma=sigma, gamma=gamma))
        self._bridge = InflationBridge(sigma_phi=sigma)
        self._cmb = CMBPredictions(sigma_phi=sigma)
        self._dm = DMPowerSpectrum(k_rig=K_RIG_MPC)
        self._entropy = EntropyOrigin(K_max=H_max, K_min=K_min, sigma=sigma)
        self._dbb = DarkBigBang(H_max=H_max, K_min=K_min, sigma=sigma, gamma=gamma)
        self._wifi = WIFIInterface()

        self._trajectory: list[dict[str, float]] = []
        self._phase_events: list[dict[str, object]] = []

    # ------------------------------------------------------------------
    # Diamond interface
    # ------------------------------------------------------------------

    def run_cycle(self, n_efolds: float = N_EFOLDS_STANDARD) -> dict[str, object]:
        """Run the Type-6 ODE for n_efolds e-folds of pre-inflationary collapse."""
        states = self._ode.integrate(H0=self._H_max, t_max=n_efolds, n_steps=int(n_efolds * 100))
        self._trajectory = [{"t": s.t, "H": s.H, "dHdt": s.dHdt} for s in states]

        self._phase_events = []
        H_star = self._ode.fixed_point()
        for s in states:
            if s.at_fixed_point:
                self._phase_events.append({
                    "type": "inflation_onset",
                    "t": s.t,
                    "H": s.H,
                    "H_star": H_star,
                })
                break

        return {
            "n_efolds_requested": n_efolds,
            "n_efolds_actual": self._ode.efolds(self._H_max),
            "H_star": H_star,
            "n_steps": len(states),
            "phase_events": len(self._phase_events),
            "tensor_scalar_r": self.tensor_to_scalar_r(),
            "dm_suppression_k": self.dm_suppression_scale(),
            "crep_gamma": self.get_crep_state()["gamma"],
            "status": "SPECULATIVE",
        }

    def get_crep_state(self) -> dict[str, float]:
        crep = CREPState()
        return {
            "C": crep.C,
            "R": crep.R,
            "E": crep.E,
            "P": crep.P,
            "gamma": crep.gamma(),
        }

    def get_utac_state(self) -> dict[str, float]:
        state = UTACState(
            H=self._H_max,
            K=self._K_min,
            sigma=self._sigma,
            beta=self._gamma,
        )
        return {
            "H": state.H,
            "r": state.r,
            "K": state.K,
            "sigma": state.sigma,
            "beta": state.beta,
            "H_star": self._ode.fixed_point(),
        }

    def get_phase_events(self) -> list[dict[str, object]]:
        return self._phase_events

    def to_zenodo_record(self) -> dict[str, object]:
        return {
            "title": "UTAC Type-6: Implosive Origin Fields (Package 33)",
            "description": (
                "SPECULATIVE pre-inflationary cosmological module. "
                "Implements reversed UTAC Type-6 ODE connected to WIFI model "
                "(Freese et al. 2023) and Dark Big Bang hypothesis. "
                "Generates falsifiable CMB and dark matter predictions."
            ),
            "zenodo_doi": ZENODO_DOI,
            "package_id": PACKAGE_REGISTRY_ID,
            "domain": "cosmology",
            "scale": "pre-inflationary",
            "predictions": {
                "tensor_scalar_r": self.tensor_to_scalar_r(),
                "dm_suppression_k_mpc_inv": self.dm_suppression_scale(),
                "bicep_compatible": self._bridge.bicep_compatible(),
            },
            "status": "speculative — not peer-reviewed",
            "keywords": [
                "UTAC", "inflation", "dark matter", "CREP", "GenesisAeon",
                "pre-inflation", "WIFI model", "Dark Big Bang",
            ],
        }

    def tensor_to_scalar_r(self) -> float:
        """Predicted tensor-to-scalar ratio r ≈ σ_Φ² ≈ 0.004 (Frame Principle)."""
        return self._bridge.frame_principle_r()

    def dm_suppression_scale(self) -> float:
        """Dark matter power-spectrum suppression wavenumber k_RIG [Mpc⁻¹]."""
        return self._dm.k_rig

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def cmb_summary(self) -> dict[str, object]:
        return self._cmb.summary()

    def dm_spectrum_summary(self) -> dict[str, object]:
        return self._dm.summary()

    def entropy_summary(self) -> dict[str, object]:
        return self._entropy.summary()

    def dark_big_bang_summary(self) -> dict[str, object]:
        return self._dbb.summary()

    def wifi_summary(self) -> dict[str, object]:
        return self._wifi.summary()
