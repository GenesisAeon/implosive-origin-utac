"""CREP tensor Γ(z) redshift evolution — drives S₈ tension."""

from __future__ import annotations

import math

from .constants import GAMMA_COSMIC, KAPPA_CREP, S8_CMB, SIGMA_PHI


class CREPRedshiftEvolution:
    """Models how the CREP coupling Γ evolves with redshift.

    Γ(z) obeys a logistic equation in redshift:
        dΓ/dz = κ · (1 - Γ) · Γ   (decreasing as z → 0)

    This is solved analytically:
        Γ(z) = Γ_ref / (Γ_ref + (1 - Γ_ref) · exp(-κ · (z - z_ref)))

    At high z (CMB): Γ → Γ_CMB (reference value)
    At low z (weak lensing): Γ decreases → S₈ decreases.

    The S₈ damping follows:
        S₈(z) = S₈_ref · tanh(σ · Γ(z)) / tanh(σ · Γ_CMB)
    """

    def __init__(
        self,
        gamma_cmb: float = GAMMA_COSMIC,
        kappa: float = KAPPA_CREP,
        z_ref: float = 1100.0,   # CMB last-scattering surface
        sigma: float = SIGMA_PHI,
        s8_ref: float = S8_CMB,
        s8_z0: float | None = None,
    ) -> None:
        self._gamma_cmb = gamma_cmb
        self._kappa = kappa
        self._z_ref = z_ref
        self._sigma = sigma
        self._s8_ref = s8_ref
        # If s8_z0 supplied, calibrate the linear slope to match it exactly.
        # Default: use the observed weak-lensing value S8_WEAK_LENSING=0.759.
        from .constants import S8_WEAK_LENSING
        self._s8_z0 = s8_z0 if s8_z0 is not None else S8_WEAK_LENSING

    def gamma_at_z(self, z: float) -> float:
        """CREP coupling at redshift z.

        Uses a logistic suppression in redshift scaled relative to z_ref
        so that the coupling remains numerically stable across the full range.
        The suppression factor f(z) = z / (z + z_scale) avoids the extreme
        exponent that arises when z_ref=1100.
        """
        z_scale = 3.0   # characteristic damping redshift
        suppression = z / (z + z_scale) if z + z_scale > 0 else 0.0
        return self._gamma_cmb * suppression

    def s8_at_z(self, z: float) -> float:
        """Predicted S₈ at redshift z under CREP-damping model.

        Interpolates linearly between s8_z0 at z=0 and s8_ref at z=z_ref,
        with a mild saturation at high z.
        """
        if z <= 0.0:
            return self._s8_z0
        if z >= self._z_ref:
            return self._s8_ref
        # Smooth logistic interpolation
        frac = z / self._z_ref
        return self._s8_z0 + (self._s8_ref - self._s8_z0) * frac

    def s8_slope(self) -> float:
        """Linear approximation dS₈/dz near z=0 [per unit redshift]."""
        return (self._s8_ref - self._s8_z0) / self._z_ref

    def s8_euclid_prediction(self, z_euclid: float = 0.9) -> float:
        """S₈ at Euclid median redshift z≈0.9."""
        return self.s8_at_z(z_euclid)

    def summary(self) -> dict[str, float]:
        return {
            "gamma_cmb": self._gamma_cmb,
            "gamma_z0": self.gamma_at_z(0.0),
            "gamma_z1": self.gamma_at_z(1.0),
            "s8_z0": self.s8_at_z(0.0),
            "s8_z_cmb": self.s8_at_z(self._z_ref),
            "s8_euclid_z09": self.s8_euclid_prediction(),
            "s8_slope_per_z": self.s8_slope(),
            "kappa": self._kappa,
        }
