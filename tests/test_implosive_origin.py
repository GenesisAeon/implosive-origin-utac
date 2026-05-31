"""Tests for UTAC Type-6: Implosive Origin Fields (Package 33)."""

from __future__ import annotations

import math

import pytest

from implosive_origin import (
    ImplosiveOriginUTAC,
    TYPE6_TARGETS,
    Type6ODE,
    Type6ODEParams,
    InflationBridge,
    CMBPredictions,
    DMPowerSpectrum,
    EntropyOrigin,
    DarkBigBang,
    PHI,
    SIGMA_PHI,
    V_RIG_KM_S,
    R_PREDICTED,
    K_RIG_MPC,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

def test_phi_value():
    assert abs(PHI - 1.6180339887) < 1e-7


def test_sigma_phi():
    assert abs(SIGMA_PHI - 1.0 / 16.0) < 1e-10


def test_v_rig_range():
    # v_RIG ≈ 1352 km/s — within 5% tolerance
    assert 1300 < V_RIG_KM_S < 1420


def test_r_predicted():
    assert abs(R_PREDICTED - SIGMA_PHI**2) < 1e-10


def test_k_rig_range():
    # k_RIG = v_RIG · H₀ / c ≈ 0.304 Mpc⁻¹
    assert 0.20 < K_RIG_MPC < 0.45


# ---------------------------------------------------------------------------
# Type6ODE
# ---------------------------------------------------------------------------

def test_type6_fixed_point_positive():
    ode = Type6ODE()
    H_star = ode.fixed_point()
    assert H_star > 0


def test_type6_dHdt_negative_above_Kmin():
    """dH/dt < 0 for H > K_min: implosive collapse toward H*."""
    ode = Type6ODE(Type6ODEParams(K_min=0.01))
    # H=1.0 >> K_min=0.01 → dH/dt = -r·H·(1 - K_min/H)·tanh < 0
    assert ode.dHdt(1.0) < 0


def test_type6_dHdt_positive_below_Kmin():
    """dH/dt > 0 for H < K_min: restoring force back to K_min."""
    ode = Type6ODE(Type6ODEParams(K_min=0.5))
    # H=0.01 < K_min=0.5 → (1 - 0.5/0.01) < 0 → -r·H·negative > 0
    assert ode.dHdt(0.01) > 0


def test_type6_integration_decreasing():
    ode = Type6ODE()
    states = ode.integrate(H0=1.0, t_max=10.0, n_steps=100)
    assert states[0].H > states[-1].H


def test_type6_efolds_positive():
    ode = Type6ODE()
    efolds = ode.efolds(H0=1.0)
    assert efolds > 0


def test_type6_efolds_range():
    """e-folds should be in a physically plausible range."""
    ode = Type6ODE(Type6ODEParams(K_min=0.01))
    efolds = ode.efolds(H0=1.0)
    # ln(1/0.01) * tanh(...) ≈ 4.6 adjusted by activation
    assert 2.0 < efolds < 10.0


# ---------------------------------------------------------------------------
# InflationBridge
# ---------------------------------------------------------------------------

def test_slow_roll_epsilon():
    bridge = InflationBridge()
    assert abs(bridge.slow_roll_epsilon() - SIGMA_PHI**2) < 1e-10


def test_r_frame_principle_value():
    bridge = InflationBridge()
    r = bridge.frame_principle_r()
    assert abs(r - 0.003906) < 1e-4


def test_bicep_compatible():
    bridge = InflationBridge()
    assert bridge.bicep_compatible() is True


def test_k_rig():
    bridge = InflationBridge()
    assert bridge.k_rig_suppression() == pytest.approx(K_RIG_MPC, rel=1e-3)


# ---------------------------------------------------------------------------
# CMBPredictions
# ---------------------------------------------------------------------------

def test_cmb_r_below_bicep():
    cmb = CMBPredictions()
    assert cmb.r_frame_principle() < 0.036


def test_cmb_litebird_detectable():
    cmb = CMBPredictions()
    assert cmb.litebird_detectable(sigma_r=0.001) is True


def test_cmb_n_s_near_one():
    cmb = CMBPredictions()
    n_s = cmb.n_s_estimate()
    assert 0.98 < n_s < 1.01


# ---------------------------------------------------------------------------
# DMPowerSpectrum
# ---------------------------------------------------------------------------

def test_dm_transfer_unity_at_zero():
    dm = DMPowerSpectrum()
    assert dm.transfer_function(0.0) == pytest.approx(1.0)


def test_dm_transfer_suppressed_at_high_k():
    dm = DMPowerSpectrum()
    # At k = 10 * k_RIG, suppression should be significant
    assert dm.transfer_function(10.0 * dm.k_rig) < 0.1


def test_dm_suppression_half_at_k_rig():
    """At k = k_RIG: T²(k_RIG) = 0.5."""
    dm = DMPowerSpectrum(n_suppression=2.0)
    ratio = dm.power_ratio(dm.k_rig)
    assert abs(ratio - 0.5) < 0.01


# ---------------------------------------------------------------------------
# EntropyOrigin
# ---------------------------------------------------------------------------

def test_entropy_positive():
    ent = EntropyOrigin()
    assert ent.entropy(1.0) >= 0
    assert ent.entropy(0.5) > 0


def test_entropy_zero_at_one():
    """S_pre(K=1) = 1 · |ln(1)| = 0."""
    ent = EntropyOrigin()
    assert ent.entropy(1.0) == pytest.approx(0.0, abs=1e-10)


def test_entropy_ratio_gt_one():
    # K_max=10 >> K_min=0.01: S(10)=10*ln10 >> S(0.01)=0.01*|ln0.01|
    ent = EntropyOrigin(K_max=10.0, K_min=0.01)
    assert ent.entropy_ratio() > 1.0


# ---------------------------------------------------------------------------
# DarkBigBang
# ---------------------------------------------------------------------------

def test_dbb_H_star_positive():
    dbb = DarkBigBang()
    assert dbb.H_star() > 0


def test_dbb_epoch_classification():
    dbb = DarkBigBang()
    H_star = dbb.H_star()
    assert dbb.epoch(100.0 * H_star).epoch == "pre-dark"
    assert dbb.epoch(H_star * 0.9).epoch == "post-threshold"
    assert dbb.epoch(H_star * 0.9).is_observable is True


def test_dbb_entropy_ratio():
    dbb = DarkBigBang(H_max=10.0, K_min=0.01)
    ratio = dbb.de_sitter_entropy_ratio()
    assert ratio > 1.0


# ---------------------------------------------------------------------------
# ImplosiveOriginUTAC (Diamond interface)
# ---------------------------------------------------------------------------

def test_diamond_run_cycle():
    system = ImplosiveOriginUTAC()
    result = system.run_cycle(n_efolds=10.0)
    assert "tensor_scalar_r" in result
    assert "dm_suppression_k" in result
    assert result["status"] == "SPECULATIVE"


def test_diamond_crep_state():
    system = ImplosiveOriginUTAC()
    crep = system.get_crep_state()
    assert 0 < crep["gamma"] < 1


def test_diamond_utac_state():
    system = ImplosiveOriginUTAC()
    utac = system.get_utac_state()
    assert utac["H_star"] > 0


def test_diamond_tensor_to_scalar_r():
    system = ImplosiveOriginUTAC()
    r = system.tensor_to_scalar_r()
    # Must be within TYPE6_TARGETS tolerance
    target, tol = TYPE6_TARGETS["tensor_scalar_r"]
    assert abs(r - target) < tol


def test_diamond_dm_suppression_scale():
    system = ImplosiveOriginUTAC()
    k = system.dm_suppression_scale()
    target, tol = TYPE6_TARGETS["dm_k_suppression_mpc_inv"]
    assert abs(k - target) < tol


def test_diamond_zenodo_record():
    system = ImplosiveOriginUTAC()
    record = system.to_zenodo_record()
    assert record["package_id"] == 33
    assert "predictions" in record
    assert "status" in record


def test_type6_targets_structure():
    for key, val in TYPE6_TARGETS.items():
        assert isinstance(val, tuple)
        assert len(val) == 2
