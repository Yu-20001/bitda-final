# AMM Monte Carlo Risk Analysis Design

## Objective

Extend the deterministic AMM comparison with a reproducible Monte Carlo
analysis of LP-return distributions under uncertain volatile-asset price
paths. The extension answers how volatility changes downside risk and fixed
Uniswap V3 range exposure without replacing the controlled deterministic
results.

## Scope

The analysis compares six configurations:

- Uniswap V2
- Uniswap V3 narrow `[0.95, 1.05]`
- Uniswap V3 medium `[0.80, 1.20]`
- Uniswap V3 wide `[0.50, 2.00]`
- Balancer weighted pool `50/50`
- Balancer weighted pool `80/20`

StableSwap is excluded because an unrestricted geometric Brownian motion does
not represent stable-asset mean reversion or jump-depeg behavior. StableSwap
remains covered by the deterministic near-parity scenarios.

## Price Process

Generate 30-day daily price paths with zero-drift geometric Brownian motion:

`P[t+1] = P[t] * exp(-0.5 * sigma_daily^2 + sigma_daily * Z[t])`

where `Z[t]` is standard normal and `sigma_daily = sigma_annual / sqrt(365)`.
Each path begins at price one.

Use:

- Annualized volatility: `20%`, `60%`, and `100%`
- Paths per volatility: `10,000`
- Steps per path: `30`
- Seed: `20260611`
- Daily volume: `50%` of TVL

The three volatility levels represent low, moderate, and high volatile-asset
markets. Zero drift avoids embedding a directional forecast. Thirty daily
steps match the base LP-return period and keep path availability transparent.
Ten thousand paths balance stable distribution summaries with a short,
repeatable runtime. A fixed seed makes every generated result auditable.

## Return Calculation

For every simulated path and configuration:

1. Calculate terminal impermanent loss with the existing analytical position
   valuation and hold benchmark.
2. Calculate gross 30-day fee return from the existing deterministic fee
   formula.
3. Give full-range models full fee availability.
4. For V3, multiply fee return by the fraction of observed daily prices,
   excluding the initial price, that lie inside the fixed range.
5. Calculate absolute LP return relative to initial capital and excess return
   relative to holding the same initial assets.

A fixed V3 position can earn fees again if a path re-enters its range. The
analysis excludes active rebalancing, gas, endogenous volume, fee compounding,
and intraday range crossings.

## Summary Outputs

Create one summary row per configuration and volatility, for 18 rows total.
Each row reports:

- `model`
- `configuration`
- `annual_volatility`
- `paths`
- `mean_terminal_price`
- `mean_impermanent_loss`
- `mean_fee_return`
- `mean_absolute_lp_return`
- `median_absolute_lp_return`
- `p05_absolute_lp_return`
- `mean_excess_return_vs_hold`
- `median_excess_return_vs_hold`
- `p05_excess_return_vs_hold`
- `underperformance_probability`
- `ever_exit_probability`
- `mean_in_range_fraction`

For full-range models, `ever_exit_probability` is zero and
`mean_in_range_fraction` is one.

## Architecture

- Add `src/amm_sim/monte_carlo.py` for GBM path generation and summary
  calculation.
- Extend `config/scenarios.yaml` with Monte Carlo assumptions.
- Extend `src/amm_sim/experiments.py` to generate the summary CSV.
- Extend `src/amm_sim/plotting.py` with return-risk and V3 range-risk figures.
- Reuse the existing experiment entry point.
- Add an independent report chapter titled `Monte Carlo Risk Analysis`.

Only the compact summary CSV is stored. Raw path-level output is regenerated
from the fixed seed when needed.

## Testing

Automated tests verify:

- Fixed-seed path generation is deterministic.
- Zero volatility produces prices equal to one.
- Path array dimensions include the initial price.
- Summary output has 18 rows and all required columns.
- Summary output contains no missing values.
- Zero-volatility IL is zero and V3 remains in range.
- V3 exit probability does not decrease as volatility rises.
- Required Monte Carlo figure files are generated.

## Report Integration

The report adds a dedicated chapter explaining:

- Why GBM, zero drift, the selected volatility levels, 10,000 paths, and the
  fixed seed were chosen.
- How path-based V3 fee availability differs from the deterministic
  linear-path approximation.
- Distributional results and downside risk.
- Why StableSwap is excluded.
- Limitations of GBM and fixed-volume fee assumptions.

The compiled report should use natural page flow and keep all figure labels
readable without padding to a target page count.

## Acceptance Criteria

- All existing and new tests pass.
- The experiment command generates `monte_carlo_summary.csv` with 18 complete
  rows and two new figures.
- Results reproduce exactly with the fixed seed.
- The report compiles with a readable new chapter and no forced page-count
  padding.
- README reproduction commands regenerate all base and Monte Carlo outputs.
