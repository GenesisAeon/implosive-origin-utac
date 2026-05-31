"""implosive-origin-utac — UTAC Type-6: Implosive Origin Fields (GenesisAeon P33).

STATUS: SPECULATIVE cosmological module. See DISCLAIMER.md.
DOI: 10.5281/zenodo.17472834
"""

from .cmb_predictions import CMBPredictions
from .constants import (
    GAMMA_INFLATION,
    K_RIG_MPC,
    PHI,
    R_PREDICTED,
    SIGMA_PHI,
    V_RIG_KM_S,
)
from .dark_big_bang import DarkBigBang
from .dm_power_spectrum import DMPowerSpectrum
from .entropy_origin import EntropyOrigin
from .inflation_bridge import InflationBridge
from .system import PACKAGE_REGISTRY, TYPE6_TARGETS, ImplosiveOriginUTAC
from .type6_ode import Type6ODE, Type6ODEParams
from .wifi_interface import WIFIInterface

__version__ = "0.1.0"

__all__ = [
    "ImplosiveOriginUTAC",
    "TYPE6_TARGETS",
    "PACKAGE_REGISTRY",
    "Type6ODE",
    "Type6ODEParams",
    "InflationBridge",
    "CMBPredictions",
    "DMPowerSpectrum",
    "EntropyOrigin",
    "DarkBigBang",
    "WIFIInterface",
    "PHI",
    "SIGMA_PHI",
    "V_RIG_KM_S",
    "R_PREDICTED",
    "K_RIG_MPC",
    "GAMMA_INFLATION",
]
