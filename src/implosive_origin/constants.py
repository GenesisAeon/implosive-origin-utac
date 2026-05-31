"""Physical and mathematical constants for UTAC Type-6."""

from __future__ import annotations

import math

# Golden ratio
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0  # 1.6180339887...

# Frame Principle: σ_Φ ≈ 1/16
SIGMA_PHI: float = 1.0 / 16.0

# CODATA 2018 fine-structure constant
ALPHA: float = 1.0 / 137.035999084

# Speed of light [km/s]
C_KM_S: float = 299_792.458

# v_RIG = c / (α⁻¹ · Φ) [km/s]
V_RIG_KM_S: float = C_KM_S / (137.035999084 * PHI)  # ≈ 1352.12 km/s

# Hubble constant [km/s/Mpc] — Planck 2018
H0_PLANCK: float = 67.4

# Current upper bound on tensor-to-scalar ratio r (BICEP/Keck 2021)
R_BICEP_UPPER: float = 0.036

# UTAC Type-6 prediction for r from Frame Principle: r ≈ σ_Φ²
R_PREDICTED: float = SIGMA_PHI**2  # ≈ 0.003906

# Standard number of inflationary e-folds
N_EFOLDS_STANDARD: float = 60.0

# Planck mass [GeV/c²] — used for K_UTAC ↔ M_P mapping
M_PLANCK_GEV: float = 1.220890e19

# k_RIG: dark matter power spectrum suppression scale [Mpc⁻¹]
# k_RIG = v_RIG · H₀ / c  [exact formula gives ≈ 0.304 Mpc⁻¹]
K_RIG_MPC: float = (V_RIG_KM_S * H0_PLANCK) / C_KM_S  # ≈ 0.304 Mpc⁻¹

# CREP Γ value for a maximally coupled inflationary system
GAMMA_INFLATION: float = 0.5 * (PHI - 1.0)  # ≈ 0.309 (golden ratio related)

PACKAGE_REGISTRY_ID: int = 33
ZENODO_DOI: str = "10.5281/zenodo.17472834"
