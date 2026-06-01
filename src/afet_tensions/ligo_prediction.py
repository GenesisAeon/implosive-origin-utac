"""LIGO O5 gravitational wave background prediction from AFET β-hierarchy."""

from __future__ import annotations

from .constants import H0_REF, OMEGA_RIG_HZ


class LIGOPrediction:
    """AFET prediction for gravitational wave background modulation.

    The β-hierarchy creates a "breathing mode" in the cosmic expansion:
        ω_RIG = v_RIG · H₀ / c  [normalised to Hz]

    This breathing mode should modulate the stochastic GW background
    at ω_RIG ≈ 0.018 Hz — within LIGO O5 sensitivity range.

    FALSIFIABLE: if LIGO O5 detects NO spectral feature at 0.018 ± 0.002 Hz
    in the stochastic GW background, the AFET breathing-mode prediction fails.
    """

    def __init__(
        self,
        omega_rig: float = OMEGA_RIG_HZ,
        h0: float = H0_REF,
    ) -> None:
        self._omega_rig = omega_rig
        self._h0 = h0

    def breathing_frequency(self) -> float:
        """Predicted GW background modulation frequency [Hz]."""
        return self._omega_rig

    def frequency_band(self, n_sigma: float = 1.0) -> tuple[float, float]:
        """Expected frequency band [Hz] for LIGO O5 search."""
        delta = 0.002 * n_sigma
        return (self._omega_rig - delta, self._omega_rig + delta)

    def ligo_o5_detectable(self) -> bool:
        """True if ω_RIG falls within LIGO O5 stochastic search band [0.01, 0.1] Hz."""
        lo, hi = 0.01, 0.1
        return lo <= self._omega_rig <= hi

    def summary(self) -> dict[str, object]:
        lo, hi = self.frequency_band()
        return {
            "omega_rig_hz": self._omega_rig,
            "band_low_hz": lo,
            "band_high_hz": hi,
            "ligo_o5_detectable": self.ligo_o5_detectable(),
            "target_dataset": "LIGO O5 stochastic GW background",
            "falsification_criterion": "no spectral feature at 0.018±0.002 Hz",
        }
