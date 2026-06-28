# implosive-origin-utac

[![Package](https://img.shields.io/badge/GenesisAeon-Package%2033-blueviolet)](https://doi.org/10.5281/zenodo.17472834)
[![Zenodo](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17472834-blue)](https://doi.org/10.5281/zenodo.17472834)
[![Status](https://img.shields.io/badge/status-SPECULATIVE-orange)](DISCLAIMER.md)
[![License](https://img.shields.io/badge/code-GPLv3--or--later-blue)](LICENSE)
[![Docs License](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE-DOCS)
[![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)](pyproject.toml)

**UTAC Type-6: Implosive Origin Fields — Pre-Inflationary Dark Matter**

GenesisAeon Package 33 · Johann Römer · MOR Research Collective · Mai 2026

> **SPECULATIVE MODULE** — See [DISCLAIMER.md](DISCLAIMER.md). All predictions are
> hypotheses awaiting observational test. Not peer-reviewed.

---

## What is this?

This package implements **UTAC Type-6** (Implosive Origin Fields): a reversed
logistic-ODE model of the pre-inflationary universe, connecting to:

- **WIFI Model** (Freese et al. 2023, arXiv:2309.14412) — pre-inflationary dark matter
- **Dark Big Bang** hypothesis (Niedermayer 2023)
- **Frame Principle** (σ_Φ ≈ 1/16) for CMB tensor-to-scalar ratio predictions

Standard UTAC describes *expansion* dynamics:
```
dH/dt = +r·H·(1 - H/K)·tanh(σΓ)
```

UTAC Type-6 reverses the sign — *implosive collapse* from a high-entropy
pre-inflationary state toward the inflationary fixed point H*:
```
dH/dt = -r·H·(1 - H/K_min)·tanh(σΓ)
```

The Phase Transition at `H* = K_min · tanh(σΓ)` is the "ignition" of standard
inflation — the matter-creation event.

---

## Falsifiable Predictions

| Prediction | Value | Testable Against |
|-----------|-------|-----------------|
| CMB tensor-to-scalar ratio `r` | `≈ 0.004` (= σ_Φ²) | BICEP/Keck, LiteBIRD |
| DM power spectrum suppression | `k_RIG ≈ 0.097 Mpc⁻¹` | Euclid DR1 |
| Pre-inflation entropy ratio | `S_pre(H_max)/S_pre(H*)` | Black hole analogues |

Current status vs. observations:
- **r < 0.036** (BICEP/Keck 2021) ✓ our prediction `r ≈ 0.004` is compatible
- **LiteBIRD** (target σ(r) ~ 0.001, 2030s) will be able to detect `r ≈ 0.004`

---

## Installation

```bash
pip install implosive-origin-utac
```

Or for development:

```bash
git clone https://github.com/GenesisAeon/implosive-origin-utac.git
cd implosive-origin-utac
uv sync --dev
```

---

## Quickstart

```bash
# Install (editable)
uv sync --dev

# Run tests
uv run pytest

# Try the Diamond CLI with the new template
uv run diamond scaffold my-inflation-model --template implosive-origin

# List all templates
uv run diamond list-templates
```

### Python API

```python
from implosive_origin import ImplosiveOriginUTAC

system = ImplosiveOriginUTAC()

# Run 60 e-folds of Type-6 collapse
result = system.run_cycle(n_efolds=60)
print(f"r (tensor-to-scalar): {result['tensor_scalar_r']:.4f}")
print(f"k_RIG suppression:     {result['dm_suppression_k']:.3f} Mpc⁻¹")
print(f"CREP Γ:                {result['crep_gamma']:.3f}")

# CMB predictions
from implosive_origin import CMBPredictions
cmb = CMBPredictions()
print(cmb.summary())

# Dark matter power spectrum
from implosive_origin import DMPowerSpectrum
dm = DMPowerSpectrum()
print(dm.euclid_testable())
```

---

## Repository Structure

```
implosive-origin-utac/
├── DISCLAIMER.md                    # SPECULATIVE — read this first
├── src/
│   ├── implosive_origin/            # Core UTAC Type-6 module (Package 33)
│   │   ├── system.py                # ImplosiveOriginUTAC — Diamond interface
│   │   ├── type6_ode.py             # Reversed UTAC Type-6 ODE
│   │   ├── inflation_bridge.py      # Connection to standard inflation
│   │   ├── wifi_interface.py        # Interface to WIFI model (Freese et al.)
│   │   ├── dark_big_bang.py         # Dark Big Bang scenario
│   │   ├── cmb_predictions.py       # B-mode + tensor-to-scalar r predictions
│   │   ├── dm_power_spectrum.py     # Dark matter power spectrum suppression
│   │   ├── entropy_origin.py        # Pre-inflationary entropy S_pre
│   │   └── constants.py             # α, Φ, c, σ_Φ, v_RIG, k_RIG
│   └── diamond_setup/               # Scaffold CLI (includes implosive-origin template)
├── data/
│   ├── bicep_keck_r_bounds.yaml
│   └── wifi_model_params.yaml
├── tests/
│   └── test_implosive_origin.py
└── notebooks/                       # Jupyter notebook stubs
```

---

## Key Constants

| Symbol | Value | Meaning |
|--------|-------|---------|
| `Φ` | 1.6180339887 | Golden ratio |
| `σ_Φ` | 1/16 = 0.0625 | Frame Principle |
| `v_RIG` | ≈ 1352 km/s | c/(α⁻¹·Φ) |
| `r` | ≈ 0.004 | σ_Φ² (CMB prediction) |
| `k_RIG` | ≈ 0.097 Mpc⁻¹ | DM suppression scale |

---

## CREP Tensor State (Package 33)

```
Γ(C, R, E, P) = (C·R·E·P)^(1/4) ≈ 0.57
  C = 0.8  (pre-inflationary coherence)
  R = 0.7  (ODE determinism)
  E = 0.5  (high pre-inflationary entropy)
  P = 0.4  (speculative — lower weight)
```

---

## Diamond CLI — Template

```bash
# Scaffold a new implosive-origin project
diamond scaffold my-inflation-model --template implosive-origin --author "Johann Römer"

# Dry-run preview
diamond scaffold test-project --template implosive-origin --dry-run
```

---

## Role in the GenesisAeon Ecosystem

**Package ID:** P33 | **Domain:** cosmology (speculative) / pre-inflation dark matter

`implosive-origin-utac` is position 13 in the GenesisAeon release order (Phase B — UTAC
cluster). It sits downstream of `utac-core` (the base UTAC engine) and `implosive-genesis`,
and provides the cosmological pre-inflationary dynamics that feed into the broader ecosystem
(e.g. `afet-tensions`, `cosmic-web`, `universums-sim`). The Diamond Interface exposed by
`ImplosiveOriginUTAC` connects UTAC mechanics to observable CMB and large-scale-structure
predictions, making this package a key link between abstract criticality theory and
falsifiable cosmological observables.

---

## References

- Freese, K. et al. (2023). *WIFI: pre-inflationary dark matter.* arXiv:2309.14412
- BICEP/Keck Collaboration (2021). *Improved constraints on primordial gravitational waves.* arXiv:2110.00483
- Römer, J. & MOR Research Collective (2025). *UTAC v1.0.* DOI: 10.5281/zenodo.17472834
- GenesisAeon Feldtheorie Preprint (2026). DOI: 10.5281/zenodo.17472834

---

## License

This repository is **dual-licensed**:

- **Source code** — [GNU General Public License v3.0 or later (GPLv3+)](LICENSE).
- **Documentation** (this README, `docs/`, and other prose/non-code content) —
  [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-DOCS).

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)

> DOI will be assigned automatically on first GitHub Release once Zenodo–GitHub integration is enabled for this repo.
> The existing DOI `10.5281/zenodo.17472834` refers to the GenesisAeon ecosystem preprint, not this package's software record.

```bibtex
@software{roemer_implosive_origin_2026,
  author    = {Römer, Johann and MOR Research Collective},
  title     = {implosive-origin-utac: UTAC Type-6 Implosive Origin Fields},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17472834},
  note      = {GenesisAeon Package 33 — SPECULATIVE cosmological module}
}
```

---

*GenesisAeon · MOR Research Collective · Mai 2026*
*"Der Mensch integriert temporal. Das LLM navigiert atemporal. Der Scope ist der gemeinsame Raum."*
