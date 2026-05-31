"""CMB B-mode polarisation and tensor-to-scalar ratio predictions.

SPECULATIVE: All values here are theoretical predictions, not measurements.
"""

from __future__ import annotations

from .constants import R_BICEP_UPPER, SIGMA_PHI


class CMBPredictions:
    """Computes CMB predictions from the Frame Principle.

    Primary prediction: r ≈ σ_Φ² ≈ 0.004
    This lies within current BICEP/Keck bounds (r < 0.036).
    Testable against LiteBIRD (target σ(r) ~ 0.001).
    """

    def __init__(self, sigma_phi: float = SIGMA_PHI) -> None:
        self.sigma_phi = sigma_phi

    def r_frame_principle(self) -> float:
        """r = σ_Φ² from the Frame Principle."""
        return self.sigma_phi**2

    def r_consistency(self) -> float:
        """r = 16ε = 16·σ_Φ² (standard slow-roll consistency relation)."""
        return 16.0 * self.sigma_phi**2

    def n_s_estimate(self) -> float:
        """Spectral index estimate: n_s ≈ 1 - 2ε - δ.

        With ε = σ_Φ² and δ ≈ 0 (slow variation):
        n_s ≈ 1 - 2·σ_Φ² ≈ 0.9922
        Compare Planck 2018: n_s = 0.9649 ± 0.0042.
        Note: this simple estimate does not account for η; for illustration only.
        """
        return 1.0 - 2.0 * self.sigma_phi**2

    def bicep_compatible(self) -> bool:
        """True if r prediction is below BICEP/Keck 2021 upper bound."""
        return self.r_frame_principle() < R_BICEP_UPPER

    def litebird_detectable(self, sigma_r: float = 0.001) -> bool:
        """True if LiteBIRD can distinguish r from zero at this precision."""
        return self.r_frame_principle() > sigma_r

    def summary(self) -> dict[str, object]:
        return {
            "sigma_phi": self.sigma_phi,
            "r_frame_principle": self.r_frame_principle(),
            "r_consistency_relation": self.r_consistency(),
            "n_s_estimate": self.n_s_estimate(),
            "bicep_keck_upper_bound": R_BICEP_UPPER,
            "bicep_compatible": self.bicep_compatible(),
            "litebird_detectable_sigma001": self.litebird_detectable(),
            "status": "SPECULATIVE — falsifiable prediction",
        }
