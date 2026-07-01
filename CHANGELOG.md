# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.1.0] - 2026-07-01
### Changed
- `ImplosiveOriginUTAC` subclasses `diamond_setup.DiamondPackage`.
- `diamond-setup>=2.1.0` as runtime dependency; vendored `src/diamond_setup/` removed.
- `get_crep_state` / `get_utac_state` raise `NotConvergedError` before first `run_cycle`.
- UTAC keys: `{H, H_star, K_eff}`; CREP key `Gamma` (was `gamma`).

## [1.0.0] - 2026

### Changed
- Relicensed from MIT to dual-license: source code under GPLv3-or-later
  (`LICENSE`), documentation under CC BY 4.0 (`LICENSE-DOCS`).

### Added
- Initial v1.0.0 release as part of the GenesisAeon ecosystem-wide 1.0.0
  milestone.
- Standardized release tooling: `.zenodo.json`, GitHub Actions release
  workflow (`.github/workflows/release.yml`), `RELEASE_GUIDE.md`,
  `CONTRIBUTING.md`, issue/PR templates.
- Full Diamond Interface implementation: `run_cycle`, `get_crep_state`,
  `get_utac_state`, `get_phase_events`, `to_zenodo_record`.
- UTAC Type-6 reversed logistic ODE (implosive pre-inflationary collapse).
- CMB tensor-to-scalar ratio prediction (r ≈ 0.004 via Frame Principle).
- Dark matter power spectrum suppression (k_RIG ≈ 0.097 Mpc⁻¹).
- WIFI Model interface (Freese et al. 2023), Dark Big Bang scenario, entropy origin.
- Diamond scaffold CLI with `implosive-origin` project template.

### Changed
- Project metadata (`pyproject.toml`) normalized: version 1.0.0, license MIT,
  authors, `requires-python >=3.11`, GenesisAeon-ecosystem dependency pins
  (`utac-core>=1.0.0`, `implosive-genesis>=1.0.0`).
- `.zenodo.json` updated to ecosystem-standard template format, version 1.0.0.
- Release workflow expanded with canary/production separation and test suite step.
