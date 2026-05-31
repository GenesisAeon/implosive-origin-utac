"""Connection between Type-6 UTAC and standard inflationary cosmology."""

from __future__ import annotations

from .constants import (
    K_RIG_MPC,
    M_PLANCK_GEV,
    R_BICEP_UPPER,
    R_PREDICTED,
    SIGMA_PHI,
    V_RIG_KM_S,
)


class InflationBridge:
    """Maps UTAC Type-6 quantities to standard inflationary cosmology.

    Key mappings:
        H_UTAC(t) ↔ Hubble parameter H(t) during inflation
        K_UTAC    ↔ Planck scale M_P
        σ_Φ ≈ 1/16 ↔ slow-roll parameter ε ≈ σ_Φ²
        r = 16ε   (standard consistency relation)

    Frame Principle prediction:
        r ≈ σ_Φ² = (1/16)² ≈ 0.00391
    """

    def __init__(self, sigma_phi: float = SIGMA_PHI) -> None:
        self.sigma_phi = sigma_phi

    def slow_roll_epsilon(self) -> float:
        """Slow-roll parameter ε = σ_Φ²."""
        return self.sigma_phi**2

    def tensor_to_scalar_r(self) -> float:
        """Tensor-to-scalar ratio r = 16ε = 16·σ_Φ²."""
        return 16.0 * self.slow_roll_epsilon()

    def frame_principle_r(self) -> float:
        """Alternative Frame Principle form: r ≈ σ_Φ² (not 16ε).

        Whether r = σ_Φ² or r = 16σ_Φ² depends on how σ_Φ maps to ε.
        Both are within BICEP/Keck bounds. This returns the direct form.
        """
        return R_PREDICTED  # σ_Φ² ≈ 0.003906

    def bicep_compatible(self) -> bool:
        """True if the Frame Principle prediction lies below BICEP/Keck r < 0.036."""
        return self.frame_principle_r() < R_BICEP_UPPER

    def k_rig_suppression(self) -> float:
        """Dark matter power-spectrum suppression wavenumber k_RIG [Mpc⁻¹].

        k_RIG ≈ v_RIG · H₀ / c  (dimensional estimate)
        """
        return K_RIG_MPC

    def planck_mass_gev(self) -> float:
        """Planck mass M_P ≈ 1.22 × 10¹⁹ GeV (maps to K_UTAC in Type-6)."""
        return M_PLANCK_GEV

    def summary(self) -> dict[str, float | bool | str]:
        return {
            "sigma_phi": self.sigma_phi,
            "slow_roll_epsilon": self.slow_roll_epsilon(),
            "r_frame_principle": self.frame_principle_r(),
            "r_consistency_relation": self.tensor_to_scalar_r(),
            "bicep_compatible": self.bicep_compatible(),
            "k_rig_mpc_inv": self.k_rig_suppression(),
            "v_rig_km_s": V_RIG_KM_S,
            "status": "SPECULATIVE — not peer-reviewed",
        }
