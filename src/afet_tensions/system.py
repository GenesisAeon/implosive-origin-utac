"""AFETTensions — Diamond interface for Package 34."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .beta_hierarchy import BetaHierarchyModel
from .constants import (
    GAMMA_COSMIC,
    PACKAGE_REGISTRY_ID,
    SIGMA_PHI,
    TENSIONS_TARGETS,
    ZENODO_DOI,
)
from .crep_redshift import CREPRedshiftEvolution
from .desi_prediction import DESIPrediction
from .euclid_prediction import EuclidPrediction
from .hubble_tension import HubbleTension
from .ligo_prediction import LIGOPrediction
from .s8_tension import S8Tension

PACKAGE_REGISTRY: dict[str, Any] = {
    "id": PACKAGE_REGISTRY_ID,
    "name": "afet-tensions",
    "class": "AFETTensions",
    "domain": "cosmology",
    "scale": "cosmological",
    "zenodo": ZENODO_DOI,
    "reference": "AFET β-Hierarchy Analysis 2025",
}


@dataclass
class CREPState:
    """CREP tensor state for the AFET tensions system."""

    C: float = 0.75   # context continuity (cosmological coherence)
    R: float = 0.80   # reproducibility (observational consistency)
    E: float = 0.60   # entropy (structure formation complexity)
    P: float = 0.50   # productivity (prediction richness)

    def gamma(self) -> float:
        return float((self.C * self.R * self.E * self.P) ** 0.25)


@dataclass
class UTACState:
    """UTAC ODE state for the AFET tensions system."""

    H: float = 70.0   # effective H₀ [km/s/Mpc] as UTAC H-value
    r: float = 1.0
    K: float = 73.0   # carrying capacity = H0_LOCAL (late-universe attractor)
    sigma: float = SIGMA_PHI
    beta: float = GAMMA_COSMIC


class AFETTensions:
    """AFET β-Hierarchy → Cosmological Tensions (GenesisAeon Package 34).

    Diamond interface implementing:
        run_cycle, get_crep_state, get_utac_state,
        get_phase_events, to_zenodo_record,
        h0_prediction, s8_prediction.

    Falsifiable predictions for LIGO O5, Euclid DR1, DESI DR2.
    """

    def __init__(
        self,
        sigma_phi: float = SIGMA_PHI,
        gamma: float = GAMMA_COSMIC,
    ) -> None:
        self._sigma_phi = sigma_phi
        self._gamma = gamma

        self._beta_model = BetaHierarchyModel(sigma_phi=sigma_phi)
        self._crep_evol = CREPRedshiftEvolution(gamma_cmb=gamma, sigma=sigma_phi)
        self._hubble = HubbleTension(self._beta_model)
        self._s8 = S8Tension(self._crep_evol)
        self._ligo = LIGOPrediction()
        self._euclid = EuclidPrediction(self._crep_evol)
        self._desi = DESIPrediction(sigma_phi=sigma_phi)

        self._phase_events: list[dict[str, object]] = []

    # ------------------------------------------------------------------
    # Diamond interface
    # ------------------------------------------------------------------

    def run_cycle(self, z_range: tuple[float, float] = (0.0, 10.0)) -> dict[str, object]:
        """Run AFET tension analysis over the given redshift range."""
        z_min, z_max = z_range
        z_points = [z_min + (z_max - z_min) * i / 20 for i in range(21)]

        h0_profile = [{"z": z, "h0_eff": self.h0_prediction(z)} for z in z_points]
        s8_profile = [{"z": z, "s8": self.s8_prediction(z)} for z in z_points]

        # Phase event: H₀ domain switch between CMB and local epochs
        self._phase_events = [
            {
                "type": "beta_domain_switch",
                "z_low": 0.0,
                "z_high": 1100.0,
                "h0_low_z": self._beta_model.h0_local_predicted(),
                "h0_high_z": self._beta_model.h0_cmb_predicted(),
            }
        ]

        return {
            "z_range": z_range,
            "h0_ratio": self._beta_model.h0_ratio(),
            "h0_local_predicted": self._beta_model.h0_local_predicted(),
            "h0_cmb_predicted": self._beta_model.h0_cmb_predicted(),
            "s8_z0": self._crep_evol.s8_at_z(0.0),
            "s8_z_cmb": self._crep_evol.s8_at_z(1100.0),
            "ligo_omega_rig_hz": self._ligo.breathing_frequency(),
            "n_phase_events": len(self._phase_events),
            "h0_profile_n": len(h0_profile),
            "s8_profile_n": len(s8_profile),
            "crep_gamma": self.get_crep_state()["gamma"],
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
        state = UTACState()
        return {
            "H": state.H,
            "r": state.r,
            "K": state.K,
            "sigma": state.sigma,
            "beta": state.beta,
        }

    def get_phase_events(self) -> list[dict[str, object]]:
        return self._phase_events

    def to_zenodo_record(self) -> dict[str, object]:
        return {
            "title": "AFET β-Hierarchy: Cosmological Tensions (Package 34)",
            "description": (
                "AFET β-hierarchy model explaining the Hubble tension (H₀) "
                "and S₈ discrepancy via domain-dependent effective cosmological "
                "parameters. Falsifiable predictions for LIGO O5, Euclid DR1, "
                "and DESI DR2."
            ),
            "zenodo_doi": ZENODO_DOI,
            "package_id": PACKAGE_REGISTRY_ID,
            "domain": "cosmology",
            "scale": "cosmological",
            "predictions": {
                "h0_local_predicted": self._beta_model.h0_local_predicted(),
                "h0_cmb_predicted": self._beta_model.h0_cmb_predicted(),
                "s8_z0": self._crep_evol.s8_at_z(0.0),
                "ligo_omega_rig_hz": self._ligo.breathing_frequency(),
                "euclid_s8_slope": self._euclid.summary()["linear_slope_per_z"],
                "desi_bao_shift_pct": self._desi.bao_shift_percent(),
            },
            "falsification_schedule": {
                "2026": "DESI DR2 → test BAO shift",
                "2027": "Euclid DR1 → test S₈(z) redshift dependence",
                "2028": "LIGO O5 → test ω_RIG GW modulation",
            },
            "keywords": [
                "Hubble tension", "S8 tension", "AFET", "CREP", "GenesisAeon",
                "cosmological tensions", "beta hierarchy", "dark energy",
            ],
        }

    def h0_prediction(self, z: float) -> float:
        """H₀_eff at redshift z under the β-hierarchy model."""
        beta = self._beta_model.beta_from_h0(
            self._beta_model.h0_local_predicted()
            if z < 1.0
            else self._beta_model.h0_cmb_predicted()
        )
        return self._beta_model.h0_eff(beta)

    def s8_prediction(self, z: float) -> float:
        """S₈ at redshift z under the CREP-damping model."""
        return self._crep_evol.s8_at_z(z)

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    def hubble_summary(self) -> dict[str, object]:
        return self._hubble.summary()

    def s8_summary(self) -> dict[str, object]:
        return self._s8.summary()

    def ligo_summary(self) -> dict[str, object]:
        return self._ligo.summary()

    def euclid_summary(self) -> dict[str, object]:
        return self._euclid.summary()

    def desi_summary(self) -> dict[str, object]:
        return self._desi.summary()

    @property
    def targets(self) -> dict[str, tuple[float, float]]:
        return TENSIONS_TARGETS
