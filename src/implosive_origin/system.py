"""ImplosiveOriginUTAC — Diamond interface for Package 33."""

from __future__ import annotations

from typing import Any

from diamond_setup.protocol import (
    CREPState,
    DiamondPackage,
    UTACState,
    ZenodoCreator,
    ZenodoRecord,
)

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
    "dm_k_suppression_mpc_inv": (0.30, 0.10),
    "type6_fixed_point": (1.0, None),
    "bicep_compatible": (1.0, None),
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

_CREP_DEFAULTS = {"C": 0.8, "R": 0.7, "E": 0.5, "P": 0.4}


class ImplosiveOriginUTAC(DiamondPackage):
    """UTAC Type-6 — Implosive Origin Fields (GenesisAeon Package 33).

    STATUS: SPECULATIVE cosmological module. See DISCLAIMER.md.
    """

    PACKAGE_ID: int = 33

    def __init__(
        self,
        H_max: float = 1.0,
        K_min: float = 0.01,
        sigma: float = SIGMA_PHI,
        gamma: float = GAMMA_INFLATION,
    ) -> None:
        super().__init__()
        self._H_max = H_max
        self._K_min = K_min
        self._sigma = sigma
        self._gamma = gamma
        self._n_efolds = N_EFOLDS_STANDARD

        self._ode = Type6ODE(Type6ODEParams(r=1.0, K_min=K_min, sigma=sigma, gamma=gamma))
        self._bridge = InflationBridge(sigma_phi=sigma)
        self._cmb = CMBPredictions(sigma_phi=sigma)
        self._dm = DMPowerSpectrum(k_rig=K_RIG_MPC)
        self._entropy = EntropyOrigin(K_max=H_max, K_min=K_min, sigma=sigma)
        self._dbb = DarkBigBang(H_max=H_max, K_min=K_min, sigma=sigma, gamma=gamma)
        self._wifi = WIFIInterface()

        self._trajectory: list[dict[str, float]] = []
        self._phase_events: list[dict[str, object]] = []
        self._H_star: float = 0.0

    def run_cycle(self, n_efolds: float | None = None) -> dict[str, Any]:
        """Run the Type-6 ODE for *n_efolds* e-folds of pre-inflationary collapse."""
        if n_efolds is not None:
            self._n_efolds = n_efolds
        return super().run_cycle()

    def _run_cycle(self) -> dict[str, Any]:
        n_efolds = self._n_efolds
        states = self._ode.integrate(
            H0=self._H_max,
            t_max=n_efolds,
            n_steps=int(n_efolds * 100),
        )
        self._trajectory = [{"t": s.t, "H": s.H, "dHdt": s.dHdt} for s in states]

        self._phase_events = []
        self._H_star = self._ode.fixed_point()
        for s in states:
            if s.at_fixed_point:
                self._phase_events.append({
                    "type": "inflation_onset",
                    "t": s.t,
                    "H": s.H,
                    "H_star": self._H_star,
                })
                break

        crep = self._build_crep_state()
        return {
            "n_efolds_requested": n_efolds,
            "n_efolds_actual": self._ode.efolds(self._H_max),
            "H_star": self._H_star,
            "n_steps": len(states),
            "phase_events": len(self._phase_events),
            "tensor_scalar_r": self.tensor_to_scalar_r(),
            "dm_suppression_k": self.dm_suppression_scale(),
            "crep_gamma": float(crep.Gamma or 0.0),
            "status": "SPECULATIVE",
        }

    def _build_crep_state(self) -> CREPState:
        return CREPState(**_CREP_DEFAULTS)

    def _build_utac_state(self) -> UTACState:
        h_norm = min(1.0, max(0.0, self._H_max))
        h_star = self._H_star if self._cycles_completed else self._ode.fixed_point()
        h_star_norm = min(1.0, max(0.0, h_star / max(self._H_max, 1e-12)))
        return UTACState(H=h_norm, H_star=h_star_norm, K_eff=max(self._K_min, 1e-6))

    def _build_phase_events(self) -> list[dict[str, Any]]:
        return list(self._phase_events)

    def _build_zenodo_record(self) -> ZenodoRecord:
        return ZenodoRecord(
            title="UTAC Type-6: Implosive Origin Fields (Package 33)",
            description=(
                "SPECULATIVE pre-inflationary cosmological module. "
                "Implements reversed UTAC Type-6 ODE connected to WIFI model "
                "(Freese et al., arXiv:2401.17371) and Dark Big Bang hypothesis. "
                "Generates falsifiable CMB and dark matter predictions."
            ),
            creators=[
                ZenodoCreator(name="Römer, Johann", affiliation="MOR Research Collective"),
            ],
        )

    def to_zenodo_record(self) -> dict[str, Any]:
        base = super().to_zenodo_record()
        return {
            **base,
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
                "UTAC",
                "inflation",
                "dark matter",
                "CREP",
                "GenesisAeon",
                "pre-inflation",
                "WIFI model",
                "Dark Big Bang",
            ],
        }

    def tensor_to_scalar_r(self) -> float:
        """Predicted tensor-to-scalar ratio r ≈ σ_Φ² ≈ 0.004 (Frame Principle)."""
        return self._bridge.frame_principle_r()

    def dm_suppression_scale(self) -> float:
        """Dark matter power-spectrum suppression wavenumber k_RIG [Mpc⁻¹]."""
        return self._dm.k_rig

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