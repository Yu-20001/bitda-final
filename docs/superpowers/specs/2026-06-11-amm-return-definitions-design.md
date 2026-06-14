# AMM Return Definitions Design

## Objective

Report two internally consistent LP-return measures and use the HODL-relative
measure for cross-AMM comparisons.

## Definitions

For initial capital \(V_0\), terminal pool value \(V_p\), terminal value of
holding the position's initial inventory \(V_h\), and collected fee value
\(F\):

- `absolute_lp_return = (V_p + F) / V_0 - 1`
- `excess_return_vs_hold = (V_p + F) / V_h - 1`

Fees are first calculated as a fraction of initial TVL and converted to a value.
For V3, that value is multiplied by deterministic or path-observed in-range
availability.

## Reporting

Generated deterministic and Monte Carlo CSVs include both measures. The main
figures, underperformance probabilities, and comparative report discussion use
`excess_return_vs_hold`, because it isolates whether liquidity provision
outperformed holding the same initial assets. The report explicitly states that
positive excess return does not imply positive absolute investment return.

## Compatibility

The ambiguous `net_return` and Monte Carlo `*_net_return` fields are removed so
that downstream users cannot mistake the old mixed-denominator calculation for
a valid return measure.
