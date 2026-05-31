"""implosive-origin template — UTAC Type-6 pre-inflationary cosmology scaffold."""

import copy

from diamond_setup._types import TemplateDict

from .genesis import TEMPLATE as GENESIS_TEMPLATE

_extra_files = {
    "DISCLAIMER.md": """\
# DISCLAIMER — Speculative Cosmological Module

**Status: SPECULATIVE**

This module implements UTAC Type-6 (Implosive Origin Fields) — a speculative
cosmological framework. All predictions are hypotheses, not established physics.

See the parent package README for full falsification conditions.
""",
    "data/bicep_keck_r_bounds.yaml": """\
# BICEP/Keck 2021 r < 0.036 — placeholder
# Replace with actual data from arXiv:2110.00483
reference: "BICEP/Keck 2021"
r_upper_95pct: 0.036
utac_prediction:
  r_frame_principle: 0.003906
  status: "SPECULATIVE"
""",
    "src/${name_snake}/constants.py": """\
\"\"\"Physical constants for ${name}.\"\"\"
import math

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
SIGMA_PHI: float = 1.0 / 16.0
ALPHA: float = 1.0 / 137.035999084
C_KM_S: float = 299_792.458
V_RIG_KM_S: float = C_KM_S / (137.035999084 * PHI)
R_PREDICTED: float = SIGMA_PHI ** 2
K_RIG_MPC: float = (V_RIG_KM_S / C_KM_S) * 67.4
""",
    "src/${name_snake}/type6_ode.py": """\
\"\"\"UTAC Type-6: reversed logistic ODE.\"\"\"
import math
from dataclasses import dataclass


@dataclass
class Type6ODEParams:
    r: float = 1.0
    K_min: float = 0.01
    sigma: float = 0.0625
    gamma: float = 0.309


class Type6ODE:
    \"\"\"dH/dt = -r·H·(1 - H/K_min)·tanh(σΓ)\"\"\"

    def __init__(self, params: Type6ODEParams | None = None) -> None:
        self.p = params or Type6ODEParams()

    def dHdt(self, H: float) -> float:
        return -self.p.r * H * (1.0 - H / self.p.K_min) * math.tanh(self.p.sigma * self.p.gamma)

    def fixed_point(self) -> float:
        return self.p.K_min * math.tanh(self.p.sigma * self.p.gamma)

    def efolds(self, H0: float = 1.0) -> float:
        H_star = self.fixed_point()
        return math.log(H0 / H_star) if H_star > 0 else float("nan")
""",
}

_implosive: TemplateDict = copy.deepcopy(GENESIS_TEMPLATE)
_implosive["name"] = "implosive-origin"
_implosive["description"] = (
    "UTAC Type-6 Implosive Origin Fields — pre-inflationary cosmology scaffold "
    "(GenesisAeon Package 33, SPECULATIVE)"
)
_implosive["variables"] = GENESIS_TEMPLATE["variables"] + ["zenodo_doi"]
_implosive["defaults"] = {
    **GENESIS_TEMPLATE["defaults"],
    "metrics": "crep,type6",
    "zenodo_doi": "10.5281/zenodo.17472834",
}
_implosive["files"] = {**GENESIS_TEMPLATE["files"], **_extra_files}

TEMPLATE: TemplateDict = _implosive
