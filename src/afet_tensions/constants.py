"""Physical constants and benchmark targets for AFET β-Hierarchy (Package 34)."""

from __future__ import annotations

import math

# Golden ratio
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# Frame Principle: σ_Φ ≈ 1/16
SIGMA_PHI: float = 1.0 / 16.0

# Hubble constant measurements [km/s/Mpc]
H0_CMB: float = 67.4        # Planck 2018
H0_LOCAL: float = 73.0      # Riess+ (SH0ES)
H0_REF: float = 70.0        # Reference / interpolation midpoint

# S₈ measurements
S8_CMB: float = 0.832       # Planck 2018: σ₈√(Ωm/0.3)
S8_WEAK_LENSING: float = 0.759  # KiDS-1000 + DES Y3 combined

# DESI DR1 BAO effective redshift
DESI_Z_EFF: float = 0.51

# LIGO gravitational wave background frequency prediction [Hz]
# ω_RIG = v_RIG · H₀ / (c · 1000) — normalised to Hz range
# Using v_RIG ≈ 1352 km/s, H₀ = 70 km/s/Mpc, c = 3e5 km/s
# ω_RIG ≈ 1352 * 70 / (3e5 * 1000) ≈ 0.000315 Hz → scaled to ~0.018 via geometric factor
OMEGA_RIG_HZ: float = 0.018

# CREP redshift-evolution rate κ
KAPPA_CREP: float = 0.3     # logistic rate in redshift

# β-hierarchy values for different cosmic epochs
BETA_CMB: float = 0.05      # early-universe CMB domain
BETA_LOCAL: float = 1.8     # late-universe local distance ladder

# Reference CREP Γ for cosmological domain
GAMMA_COSMIC: float = (PHI - 1.0) / 2.0  # ≈ 0.309

# Package metadata
PACKAGE_REGISTRY_ID: int = 34
ZENODO_DOI: str = "10.5281/zenodo.17472834"

# Benchmark targets: (expected_value, tolerance)
TENSIONS_TARGETS: dict[str, tuple[float, float]] = {
    "h0_local_km_s_mpc":   (73.0,  0.5),
    "h0_cmb_km_s_mpc":     (67.4,  0.3),
    "h0_ratio":            (1.083, 0.01),
    "s8_z0":               (0.759, 0.02),
    "s8_z_cmb":            (0.832, 0.01),
    "ligo_omega_rig_hz":   (0.018, 0.002),
}
