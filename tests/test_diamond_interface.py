"""Tests for the ImplosiveOriginUTAC Diamond-Template interface (Package 33)."""

from __future__ import annotations

import pytest
from diamond_setup.protocol import NotConvergedError
from diamond_setup.validation import validate_diamond_instance

from implosive_origin.system import ImplosiveOriginUTAC


@pytest.fixture(scope="module")
def origin() -> ImplosiveOriginUTAC:
    system = ImplosiveOriginUTAC()
    system.run_cycle(n_efolds=10.0)
    return system


def test_not_converged_before_run_cycle():
    pkg = ImplosiveOriginUTAC()
    with pytest.raises(NotConvergedError):
        pkg.get_crep_state()


def test_validate_diamond_instance():
    pkg = ImplosiveOriginUTAC()
    assert validate_diamond_instance(pkg) == []


def test_run_cycle_returns_dict():
    result = ImplosiveOriginUTAC().run_cycle(n_efolds=5.0)
    assert isinstance(result, dict)
    assert result["status"] == "SPECULATIVE"


def test_get_crep_state_keys(origin: ImplosiveOriginUTAC):
    state = origin.get_crep_state()
    assert set(state.keys()) == {"C", "R", "E", "P", "Gamma"}


def test_get_utac_state_keys(origin: ImplosiveOriginUTAC):
    state = origin.get_utac_state()
    assert set(state.keys()) == {"H", "H_star", "K_eff"}
    assert state["H_star"] > 0


def test_to_zenodo_record_structure(origin: ImplosiveOriginUTAC):
    record = origin.to_zenodo_record()
    for key in ("title", "description", "creators", "package_id", "predictions"):
        assert key in record
