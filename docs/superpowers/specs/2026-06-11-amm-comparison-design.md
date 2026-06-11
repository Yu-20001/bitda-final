# AMM Mechanism Comparison Design

## Objective

Build a reproducible analytical simulator and an English two-column LaTeX
report that satisfy the base requirements and report-quality portion of Topic
A:

1. Analyze the mathematical models and core mechanisms of constant-product,
   concentrated-liquidity, StableSwap, and weighted-pool AMMs.
2. Simulate different liquidity and trade-volume scenarios.
3. Visualize differences in slippage, LP return, and impermanent loss.
4. Explain methods, assumptions, results, limitations, and parameter choices
   clearly enough for an 8--10 page technical report.

The project intentionally excludes the extra-content portion: no Monte Carlo
simulation, LVR analysis, live on-chain data, active V3 rebalancing, or
interactive dashboard.

## Approach

Use a deterministic analytical simulator rather than contract forks or
notebook-only analysis. Each AMM is represented by a small, independently
tested Python module. A single experiment runner reads fixed scenarios,
produces CSV data and publication-ready figures, and supplies the evidence used
in the report.

This approach makes every result reproducible and keeps assumptions visible.
It also avoids infrastructure work that does not directly support the rubric.

## Models

### Uniswap V2

- Two-token constant-product pool: `x * y = k`.
- Default swap fee: 0.30%.
- Slippage is measured against the pre-trade spot price and includes price
  impact but reports fee separately.
- Impermanent loss is measured against holding the initial token quantities.

### Uniswap V3

- A single fixed concentrated-liquidity position using the standard virtual
  reserve formulation.
- Compare narrow, medium, and wide symmetric ranges around the initial price:
  `[0.95, 1.05]`, `[0.80, 1.20]`, and `[0.50, 2.00]`.
- Initial token value is normalized to the same capital as other models.
- No active rebalancing. A position outside its range earns no fees.
- Default swap fee: 0.30%.

The three fixed ranges isolate the capital-efficiency versus range-risk
trade-off without introducing strategy-dependent rebalancing.

### Curve StableSwap

- Two-token StableSwap invariant using equal initial balances.
- Compare amplification coefficients `A = 10, 100, 1000`.
- Used only for correlated assets near parity.
- Default swap fee: 0.04%.

These values span weak, moderate, and strong amplification and visibly show how
the invariant transitions from constant-product-like behavior toward a
constant-sum-like region near parity.

### Balancer Weighted Pool

- Two-token constant-mean invariant: `x^w_x * y^w_y = k`.
- Compare `50/50` and `80/20` weights.
- Default swap fee: 0.30%.

The `50/50` pool provides a direct constant-product baseline; the `80/20` pool
shows how asymmetric exposure changes price impact and impermanent loss.

## Metrics

### Slippage

For an exact-input swap:

`slippage = (spot_price - execution_price) / spot_price`

The experiment reports:

- Gross input
- Fee paid
- Net input
- Output amount
- Execution price
- Slippage percentage

### Impermanent Loss

For a specified terminal external price:

`IL = pool_position_value / hold_value - 1`

The comparison uses equal initial capital but preserves each pool's intended
weights. V3 positions are valued with the fixed-range inventory formulas.

### 30-Day LP Return

Use deterministic fixed-period scenarios:

- Daily volume as a fraction of TVL: `10%, 50%, 100%`
- Terminal price changes: `-50%, -20%, -5%, +5%, +20%, +50%`
- Period: 30 days

Fee income is approximated as:

`period_fee_income = daily_volume * fee_rate * 30`

For V3, fee income is multiplied by an in-range availability factor derived
from a linear path between initial and terminal price. LP net return equals fee
return plus impermanent loss. This intentionally simple decomposition is
reported as a limitation: it does not model endogenous volume, arbitrage
volume, fee compounding, or path-dependent inventory changes.

## Experimental Design

### Slippage Experiments

- TVL: `$100,000`, `$1,000,000`, `$10,000,000`
- Trade sizes: `0.1%, 0.5%, 1%, 2%, 5%, 10%, 20%` of TVL
- Models/configurations:
  - Uniswap V2
  - Uniswap V3 narrow, medium, wide
  - StableSwap `A = 10, 100, 1000`
  - Weighted Pool `50/50`, `80/20`

Trade inputs are normalized by pool value so that results can be compared
across liquidity levels. Absolute outputs still demonstrate scaling with TVL.

### IL and LP Return Experiments

- Initial TVL: `$1,000,000`
- Terminal price changes and daily-volume levels listed above
- V3 fixed ranges
- StableSwap evaluated only for the near-parity price changes `-5%` and `+5%`
  because its intended domain is correlated assets.

## Outputs

### Source and Configuration

- `src/amm_sim/`: model and metric modules
- `config/scenarios.yaml`: all experiment parameters
- `scripts/run_experiments.py`: deterministic experiment entry point
- `tests/`: model invariants, known values, and experiment smoke tests

### Generated Evidence

- CSV files for slippage, impermanent loss, and LP return
- Publication-ready PDF figures
- English two-column LaTeX report and compiled PDF
- README with setup, reproduction, and scope instructions

## Report Structure

1. Abstract
2. Introduction and research questions
3. Mathematical background
4. Methodology and parameter rationale
5. Slippage results
6. Impermanent-loss results
7. LP-return results
8. Discussion and market suitability
9. Limitations
10. Conclusion

The report will distinguish mathematical results from modeling assumptions and
will not claim that any AMM is universally superior.

## Architecture

```text
src/amm_sim/
  common.py          shared result records and validation
  uniswap_v2.py      constant-product swaps and position value
  uniswap_v3.py      fixed-range position math and swaps
  stableswap.py      two-asset invariant and swap solver
  weighted_pool.py   weighted invariant swaps and position value
  metrics.py         slippage, IL, and deterministic LP return
  experiments.py     scenario expansion and tabular outputs
tests/
scripts/run_experiments.py
config/scenarios.yaml
results/data/
results/figures/
report/main.tex
```

Each model owns only its invariant and position valuation. Cross-model metrics
and scenario orchestration remain separate so that model tests stay small and
comparisons use the same definitions.

## Testing and Verification

- Use test-driven development for production Python functions.
- Verify known constant-product and weighted-pool swap outputs.
- Verify invariants before and after swaps within numerical tolerance.
- Verify V3 inventory behavior below, inside, and above a range.
- Verify higher StableSwap amplification reduces near-parity slippage.
- Verify zero price change produces zero impermanent loss.
- Verify generated CSV files contain every expected scenario.
- Run the complete pytest suite.
- Run the experiment script from a clean results directory.
- Compile the report with Tectonic and inspect page count and PDF render.

## Acceptance Criteria

The work stops for user review when:

- All four required AMM mechanisms are implemented and tested.
- Required liquidity and volume scenarios execute deterministically.
- Slippage, LP return, and impermanent-loss CSVs and figures exist.
- The English two-column report compiles to an 8--10 page PDF.
- README reproduction commands succeed.
- No explicitly excluded extra-content feature is included.

