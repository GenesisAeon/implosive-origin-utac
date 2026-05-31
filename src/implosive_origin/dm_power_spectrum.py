"""Dark matter power spectrum suppression prediction from UTAC Type-6.

SPECULATIVE: Prediction that small-scale power is suppressed at k > k_RIG.
Testable against Euclid DR1 weak lensing.
"""

from __future__ import annotations

import math

from .constants import K_RIG_MPC, V_RIG_KM_S, H0_PLANCK, C_KM_S


class DMPowerSpectrum:
    """UTAC Type-6 prediction for dark matter power spectrum.

    Type-6 suppresses small-scale power at k > k_RIG.
    k_RIG ≈ v_RIG · H₀ / c ≈ 0.097 Mpc⁻¹

    Suppression function: P_Type6(k) = P_ΛCDM(k) · T²(k)
    Transfer function: T(k) = 1 / sqrt(1 + (k / k_RIG)^n_supp)
    """

    def __init__(
        self,
        k_rig: float = K_RIG_MPC,
        n_suppression: float = 2.0,
    ) -> None:
        self.k_rig = k_rig
        self.n_suppression = n_suppression

    def transfer_function(self, k: float) -> float:
        """T(k): multiplicative suppression at wavenumber k [Mpc⁻¹]."""
        if k <= 0:
            return 1.0
        return 1.0 / math.sqrt(1.0 + (k / self.k_rig) ** self.n_suppression)

    def power_ratio(self, k: float) -> float:
        """P_Type6(k) / P_ΛCDM(k) = T²(k)."""
        return self.transfer_function(k) ** 2

    def suppression_at_k(self, k: float) -> float:
        """Fractional suppression 1 - T²(k) at wavenumber k."""
        return 1.0 - self.power_ratio(k)

    def euclid_testable(self) -> dict[str, object]:
        """Predictions at Euclid-relevant wavenumbers."""
        ks = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
        return {
            "k_rig_mpc_inv": self.k_rig,
            "predictions": [
                {
                    "k_mpc_inv": k,
                    "transfer": round(self.transfer_function(k), 6),
                    "suppression_pct": round(self.suppression_at_k(k) * 100, 3),
                }
                for k in ks
            ],
            "status": "SPECULATIVE — testable against Euclid DR1",
        }

    def summary(self) -> dict[str, object]:
        return {
            "k_rig_mpc_inv": self.k_rig,
            "n_suppression": self.n_suppression,
            "v_rig_km_s": V_RIG_KM_S,
            "suppression_at_k_rig": self.suppression_at_k(self.k_rig),
            **self.euclid_testable(),
        }
