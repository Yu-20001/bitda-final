# Reproducible AMM Comparison

This project compares Uniswap V2, fixed-range Uniswap V3, Curve StableSwap,
and Balancer weighted pools using deterministic analytical simulations and an
additional Monte Carlo risk analysis.

## Scope

The implementation covers the Topic A base requirements:

- Mathematical models and core mechanisms for four AMM designs
- Different liquidity and normalized trade-size scenarios
- Slippage, impermanent-loss, and deterministic 30-day LP-return comparisons
- Publication-ready figures and an English two-column technical report

The additional analysis uses reproducible geometric Brownian motion paths to
compare LP-return distributions and V3 range risk. LVR, live chain data,
active V3 rebalancing, and an interactive dashboard remain excluded.

## Environment

The isolated environment is stored at `.conda-env`. Recreate it with:

```bash
mamba env create -p .conda-env -f environment.yml
```

## Reproduce

```bash
MPLCONFIGDIR=.cache/matplotlib .conda-env/bin/pytest
PYTHONPATH=src MPLCONFIGDIR=.cache/matplotlib .conda-env/bin/python scripts/run_experiments.py
cd report
XDG_CACHE_HOME=../.cache HOME=.. ../.conda-env/bin/tectonic main.tex
```

The experiment command deterministically generates:

- `results/data/slippage.csv`: 189 scenarios
- `results/data/impermanent_loss.csv`: 42 scenarios
- `results/data/lp_return.csv`: 126 scenarios
- `results/data/monte_carlo_summary.csv`: 18 distribution summaries
- `results/figures/`: seven PDF figures used by the report

The compiled report is `report/main.pdf`.

## Model Assumptions

- Initial price is one and all configurations use equal starting capital.
- V3 compares narrow, medium, and wide fixed ranges without rebalancing.
- V3 exact-input quotes that exceed a fixed range's capacity are rejected.
- StableSwap compares `A = 10, 100, 1000` only for correlated assets.
- Balancer compares `50/50` and `80/20`; swaps use token X as input.
- LP fee return uses fixed daily volume over 30 days.
- Outputs report both absolute LP return relative to initial capital and excess
  return relative to holding the same initial assets. Comparative figures and
  underperformance probabilities use excess return versus HODL.
- V3 fee availability follows a linear path from initial to terminal price.
- Monte Carlo uses 10,000 fixed-seed, zero-drift GBM paths for each annualized
  volatility level: `20%`, `60%`, and `100%`.
- Monte Carlo V3 fees use the observed daily in-range fraction.
- StableSwap is excluded from GBM because stable assets require a different
  mean-reversion and depeg process.

See `docs/superpowers/specs/2026-06-11-amm-comparison-design.md` and the report
for the rationale and limitations.
