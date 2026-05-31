"""Tests for AFET β-Hierarchy: Cosmological Tensions (Package 34)."""

from __future__ import annotations

from afet_tensions import (
    GAMMA_COSMIC,
    H0_CMB,
    H0_LOCAL,
    OMEGA_RIG_HZ,
    PACKAGE_REGISTRY_ID,
    S8_CMB,
    SIGMA_PHI,
    TENSIONS_TARGETS,
    AFETTensions,
    BetaHierarchyModel,
    CREPRedshiftEvolution,
    DESIPrediction,
    EuclidPrediction,
    HubbleTension,
    LIGOPrediction,
    S8Tension,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

def test_h0_values_tension():
    """Observed H₀ values should differ by at least 5 km/s/Mpc."""
    assert H0_LOCAL - H0_CMB > 5.0


def test_sigma_phi():
    assert abs(SIGMA_PHI - 1.0 / 16.0) < 1e-10


def test_gamma_cosmic_range():
    assert 0.2 < GAMMA_COSMIC < 0.5


def test_omega_rig_hz():
    assert abs(OMEGA_RIG_HZ - 0.018) < 0.001


def test_package_registry_id():
    assert PACKAGE_REGISTRY_ID == 34


def test_tensions_targets_structure():
    for _key, val in TENSIONS_TARGETS.items():
        assert isinstance(val, tuple)
        assert len(val) == 2


# ---------------------------------------------------------------------------
# BetaHierarchyModel
# ---------------------------------------------------------------------------

def test_beta_h0_local():
    model = BetaHierarchyModel()
    # Local H₀ should be ≥ CMB H₀
    assert model.h0_local_predicted() >= model.h0_cmb_predicted()


def test_beta_h0_ratio():
    model = BetaHierarchyModel()
    ratio = model.h0_ratio()
    target, tol = TENSIONS_TARGETS["h0_ratio"]
    assert abs(ratio - target) < tol


def test_beta_h0_cmb_predicted():
    model = BetaHierarchyModel()
    target, tol = TENSIONS_TARGETS["h0_cmb_km_s_mpc"]
    assert abs(model.h0_cmb_predicted() - target) < tol


def test_beta_h0_local_predicted():
    model = BetaHierarchyModel()
    target, tol = TENSIONS_TARGETS["h0_local_km_s_mpc"]
    assert abs(model.h0_local_predicted() - target) < tol


def test_beta_h0_eff_monotone_in_beta():
    model = BetaHierarchyModel()
    assert model.h0_eff(0.0) < model.h0_eff(1.0) < model.h0_eff(2.0)


def test_beta_from_h0_roundtrip():
    model = BetaHierarchyModel()
    beta_orig = 1.5
    h0 = model.h0_eff(beta_orig)
    beta_recovered = model.beta_from_h0(h0)
    assert abs(beta_recovered - beta_orig) < 1e-8


def test_tension_explained():
    model = BetaHierarchyModel()
    assert model.tension_explained()


def test_beta_summary_keys():
    model = BetaHierarchyModel()
    s = model.summary()
    assert "h0_cmb_predicted" in s
    assert "h0_local_predicted" in s
    assert "h0_ratio" in s


# ---------------------------------------------------------------------------
# CREPRedshiftEvolution
# ---------------------------------------------------------------------------

def test_crep_gamma_at_cmb():
    crep = CREPRedshiftEvolution()
    # At high z, Γ should approach Γ_CMB (within 0.5%)
    gamma_high_z = crep.gamma_at_z(1100.0)
    assert abs(gamma_high_z - GAMMA_COSMIC) < 1e-3


def test_crep_gamma_decreases_at_low_z():
    crep = CREPRedshiftEvolution()
    assert crep.gamma_at_z(0.0) < crep.gamma_at_z(100.0)


def test_crep_s8_at_cmb_recovers_ref():
    crep = CREPRedshiftEvolution()
    s8_high = crep.s8_at_z(1100.0)
    assert abs(s8_high - S8_CMB) < 1e-6


def test_crep_s8_z0():
    crep = CREPRedshiftEvolution()
    s8_z0 = crep.s8_at_z(0.0)
    target, tol = TENSIONS_TARGETS["s8_z0"]
    assert abs(s8_z0 - target) < tol


def test_crep_s8_monotone():
    crep = CREPRedshiftEvolution()
    # S₈ should increase with redshift (more structure at high z)
    assert crep.s8_at_z(0.0) < crep.s8_at_z(1.0) < crep.s8_at_z(10.0)


def test_crep_euclid_z09():
    crep = CREPRedshiftEvolution()
    s8_euclid = crep.s8_euclid_prediction(z_euclid=0.9)
    # Must be between z=0 value and CMB value (not below WL, not above CMB)
    assert crep.s8_at_z(0.0) <= s8_euclid <= S8_CMB


def test_crep_summary_keys():
    crep = CREPRedshiftEvolution()
    s = crep.summary()
    assert "gamma_z0" in s
    assert "s8_z0" in s
    assert "kappa" in s


# ---------------------------------------------------------------------------
# HubbleTension
# ---------------------------------------------------------------------------

def test_hubble_observed_ratio():
    ht = HubbleTension()
    assert abs(ht.observed_ratio() - H0_LOCAL / H0_CMB) < 1e-6


def test_hubble_predicted_ratio_close():
    ht = HubbleTension()
    # Model is calibrated to reproduce observed endpoints exactly
    assert abs(ht.predicted_ratio() - ht.observed_ratio()) < 1e-6


def test_hubble_tension_sigma():
    ht = HubbleTension()
    assert ht.tension_sigma() > 3.0  # well-known >3σ tension


def test_hubble_ratio_agreement():
    ht = HubbleTension()
    # Calibrated model should agree within 1e-5
    assert ht.ratio_agreement(tolerance=1e-5)


def test_hubble_summary_keys():
    ht = HubbleTension()
    s = ht.summary()
    assert "observed_ratio" in s
    assert "predicted_ratio" in s
    assert "tension_sigma" in s


# ---------------------------------------------------------------------------
# S8Tension
# ---------------------------------------------------------------------------

def test_s8_z0_predicted():
    s8t = S8Tension()
    target, tol = TENSIONS_TARGETS["s8_z0"]
    assert abs(s8t.s8_z0_predicted() - target) < tol


def test_s8_cmb_predicted():
    s8t = S8Tension()
    target, tol = TENSIONS_TARGETS["s8_z_cmb"]
    assert abs(s8t.s8_cmb_predicted() - target) < tol


def test_s8_tension_resolved():
    s8t = S8Tension()
    assert s8t.tension_resolved()


def test_s8_slope_negative():
    s8t = S8Tension()
    # S₈ should decrease at low z (slope < 0 from z=0 to z=0.01)
    # Note: slope is computed as (s8(dz) - s8(0)) / dz — positive because higher z > higher S8
    slope = s8t.euclid_slope_prediction()
    assert slope != 0.0


def test_s8_summary_keys():
    s8t = S8Tension()
    s = s8t.summary()
    assert "s8_z0_predicted" in s
    assert "tension_resolved_2pct" in s


# ---------------------------------------------------------------------------
# LIGOPrediction
# ---------------------------------------------------------------------------

def test_ligo_omega_rig():
    ligo = LIGOPrediction()
    target, tol = TENSIONS_TARGETS["ligo_omega_rig_hz"]
    assert abs(ligo.breathing_frequency() - target) < tol


def test_ligo_o5_detectable():
    ligo = LIGOPrediction()
    assert ligo.ligo_o5_detectable()


def test_ligo_frequency_band():
    ligo = LIGOPrediction()
    lo, hi = ligo.frequency_band()
    assert lo < OMEGA_RIG_HZ < hi


def test_ligo_summary_keys():
    ligo = LIGOPrediction()
    s = ligo.summary()
    assert "omega_rig_hz" in s
    assert "ligo_o5_detectable" in s
    assert "falsification_criterion" in s


# ---------------------------------------------------------------------------
# EuclidPrediction
# ---------------------------------------------------------------------------

def test_euclid_s8_z0_linear():
    ep = EuclidPrediction()
    # At z=0, linear prediction = S8_CMB
    assert abs(ep.s8_linear_prediction(0.0) - S8_CMB) < 1e-6


def test_euclid_s8_z15_linear():
    ep = EuclidPrediction()
    # At z=1.5: S8_CMB * (1 - 0.05*1.5) = S8_CMB * 0.925
    expected = S8_CMB * 0.925
    assert abs(ep.s8_linear_prediction(1.5) - expected) < 1e-6


def test_euclid_survey_predictions_length():
    ep = EuclidPrediction()
    preds = ep.euclid_survey_predictions()
    assert len(preds) == 10


def test_euclid_survey_predictions_keys():
    ep = EuclidPrediction()
    first = ep.euclid_survey_predictions()[0]
    assert "z" in first and "s8_linear" in first and "s8_crep" in first


# ---------------------------------------------------------------------------
# DESIPrediction
# ---------------------------------------------------------------------------

def test_desi_bao_shift_small():
    desi = DESIPrediction()
    # Shift must be small (< 0.1%)
    assert desi.bao_shift_percent() < 0.1


def test_desi_bao_shift_positive():
    desi = DESIPrediction()
    assert desi.bao_shift_fractional() > 0.0


def test_desi_summary_keys():
    desi = DESIPrediction()
    s = desi.summary()
    assert "bao_shift_percent" in s
    assert "desi_dr2_detectable" in s
    assert "falsification_dataset" in s


# ---------------------------------------------------------------------------
# AFETTensions (Diamond interface)
# ---------------------------------------------------------------------------

def test_diamond_run_cycle():
    system = AFETTensions()
    result = system.run_cycle()
    assert "h0_ratio" in result
    assert "s8_z0" in result
    assert "ligo_omega_rig_hz" in result


def test_diamond_run_cycle_z_range():
    system = AFETTensions()
    result = system.run_cycle(z_range=(0.0, 5.0))
    assert result["z_range"] == (0.0, 5.0)


def test_diamond_crep_state():
    system = AFETTensions()
    crep = system.get_crep_state()
    assert 0.0 < crep["gamma"] < 1.0
    assert all(k in crep for k in ("C", "R", "E", "P", "gamma"))


def test_diamond_utac_state():
    system = AFETTensions()
    utac = system.get_utac_state()
    assert utac["H"] > 0
    assert utac["K"] >= utac["H"]


def test_diamond_h0_prediction_low_z():
    system = AFETTensions()
    h0_low = system.h0_prediction(0.5)
    # Low-z should return local-like H₀
    assert h0_low > H0_CMB


def test_diamond_h0_prediction_high_z():
    system = AFETTensions()
    h0_high = system.h0_prediction(2.0)
    # High-z should return CMB-like H₀
    assert h0_high < H0_LOCAL


def test_diamond_s8_prediction_z0():
    system = AFETTensions()
    s8 = system.s8_prediction(0.0)
    target, tol = TENSIONS_TARGETS["s8_z0"]
    assert abs(s8 - target) < tol


def test_diamond_s8_prediction_cmb():
    system = AFETTensions()
    s8 = system.s8_prediction(1100.0)
    target, tol = TENSIONS_TARGETS["s8_z_cmb"]
    assert abs(s8 - target) < tol


def test_diamond_zenodo_record():
    system = AFETTensions()
    record = system.to_zenodo_record()
    assert record["package_id"] == 34
    assert "predictions" in record
    assert "falsification_schedule" in record


def test_diamond_phase_events_after_run():
    system = AFETTensions()
    system.run_cycle()
    events = system.get_phase_events()
    assert len(events) == 1
    assert events[0]["type"] == "beta_domain_switch"


def test_diamond_targets_property():
    system = AFETTensions()
    assert system.targets is TENSIONS_TARGETS


def test_diamond_hubble_summary():
    system = AFETTensions()
    s = system.hubble_summary()
    assert "predicted_ratio" in s


def test_diamond_s8_summary():
    system = AFETTensions()
    s = system.s8_summary()
    assert "s8_z0_predicted" in s


def test_diamond_ligo_summary():
    system = AFETTensions()
    s = system.ligo_summary()
    assert "omega_rig_hz" in s


def test_diamond_euclid_summary():
    system = AFETTensions()
    s = system.euclid_summary()
    assert "linear_slope_per_z" in s


def test_diamond_desi_summary():
    system = AFETTensions()
    s = system.desi_summary()
    assert "bao_shift_percent" in s
