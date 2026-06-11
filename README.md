# Deterministic AMM Comparison

This project compares Uniswap V2, fixed-range Uniswap V3, Curve StableSwap,
and Balancer weighted pools using reproducible analytical simulations.

## Scope

The implementation covers the Topic A base requirements:

- Mathematical models and core mechanisms for four AMM designs
- Different liquidity and normalized trade-size scenarios
- Slippage, impermanent-loss, and deterministic 30-day LP-return comparisons
- Publication-ready figures and an English two-column technical report

The current scope stops at the base implementation and report-quality work.
Monte Carlo simulation, LVR, live chain data, active V3 rebalancing, and an
interactive dashboard are intentionally excluded.

## Environment

The isolated environment is stored at `.conda-env`. Recreate it with:

```bash
mamba env create -p .conda-env -f environment.yml
```

## Reproduce

```bash
MPLCONFIGDIR=.cache/matplotlib .conda-env/bin/pytest
MPLCONFIGDIR=.cache/matplotlib .conda-env/bin/python scripts/run_experiments.py
cd report
XDG_CACHE_HOME=../.cache HOME=.. ../.conda-env/bin/tectonic main.tex
```

The experiment command deterministically generates:

- `results/data/slippage.csv`: 189 scenarios
- `results/data/impermanent_loss.csv`: 42 scenarios
- `results/data/lp_return.csv`: 126 scenarios
- `results/figures/`: five PDF figures used by the report

The compiled report is `report/main.pdf`.

## Model Assumptions

- Initial price is one and all configurations use equal starting capital.
- V3 compares narrow, medium, and wide fixed ranges without rebalancing.
- StableSwap compares `A = 10, 100, 1000` only for correlated assets.
- Balancer compares `50/50` and `80/20`; swaps use token X as input.
- LP fee return uses fixed daily volume over 30 days.
- V3 fee availability follows a linear path from initial to terminal price.

See `docs/superpowers/specs/2026-06-11-amm-comparison-design.md` and the report
for the rationale and limitations.
