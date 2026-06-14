# AMM Mechanism Comparison Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and document a deterministic simulator comparing Uniswap V2,
Uniswap V3 fixed ranges, Curve StableSwap, and Balancer weighted pools.

**Architecture:** Keep invariant math in four independent model modules, place
cross-model metric definitions in one metrics module, and let one experiment
module expand a YAML scenario matrix into CSVs and figures. The LaTeX report
uses only generated evidence and explicitly states simplifying assumptions.

**Tech Stack:** Python 3.12, NumPy, Pandas, SciPy, Matplotlib, PyYAML, pytest,
Tectonic LaTeX.

---

### Task 1: Project Skeleton and Reproduction Contract

**Files:**
- Create: `pyproject.toml`
- Create: `environment.yml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `src/amm_sim/__init__.py`
- Create: `tests/test_package.py`

- [ ] Write a failing package-import test.
- [ ] Run `.conda-env/bin/pytest tests/test_package.py -v` and confirm the
  package is missing.
- [ ] Add the minimal package skeleton and pytest path configuration.
- [ ] Re-run the package test and confirm it passes.
- [ ] Document environment and reproduction commands without claiming results.

### Task 2: Uniswap V2 Model

**Files:**
- Create: `src/amm_sim/common.py`
- Create: `src/amm_sim/uniswap_v2.py`
- Create: `tests/test_uniswap_v2.py`

- [ ] Write failing tests for spot price, exact-input output, fee amount,
  invariant preservation, and terminal position value.
- [ ] Run the focused tests and confirm expected failures.
- [ ] Implement the smallest constant-product model that passes the tests.
- [ ] Run focused and complete tests.

### Task 3: Balancer Weighted-Pool Model

**Files:**
- Create: `src/amm_sim/weighted_pool.py`
- Create: `tests/test_weighted_pool.py`

- [ ] Write failing tests for weighted spot price, `50/50` equivalence to
  constant product, `80/20` output, invariant preservation, and terminal value.
- [ ] Confirm focused tests fail for missing behavior.
- [ ] Implement weighted-pool swap and valuation formulas.
- [ ] Run focused and complete tests.

### Task 4: Uniswap V3 Fixed-Range Model

**Files:**
- Create: `src/amm_sim/uniswap_v3.py`
- Create: `tests/test_uniswap_v3.py`

- [ ] Write failing tests for normalized liquidity, inventory below/inside/above
  a range, capital normalization, swap output, and out-of-range availability.
- [ ] Confirm focused tests fail for missing behavior.
- [ ] Implement fixed-range virtual-reserve math without active rebalancing.
- [ ] Run focused and complete tests.

### Task 5: Two-Asset StableSwap Model

**Files:**
- Create: `src/amm_sim/stableswap.py`
- Create: `tests/test_stableswap.py`

- [ ] Write failing tests for invariant calculation, swap conservation,
  near-parity output, and decreasing slippage for increasing `A`.
- [ ] Confirm focused tests fail for missing behavior.
- [ ] Implement the two-asset StableSwap invariant and iterative `y` solver.
- [ ] Run focused and complete tests.

### Task 6: Shared Metrics

**Files:**
- Create: `src/amm_sim/metrics.py`
- Create: `tests/test_metrics.py`

- [ ] Write failing tests for slippage, zero-change IL, known V2 IL,
  deterministic fee return, V3 availability, absolute LP return, and excess
  return versus HODL.
- [ ] Confirm focused tests fail for missing behavior.
- [ ] Implement only the shared metric functions required by the tests.
- [ ] Run focused and complete tests.

### Task 7: Scenario Expansion and CSV Generation

**Files:**
- Create: `config/scenarios.yaml`
- Create: `src/amm_sim/experiments.py`
- Create: `scripts/run_experiments.py`
- Create: `tests/test_experiments.py`

- [ ] Write failing tests for expected configuration values, scenario counts,
  deterministic output, and required CSV columns.
- [ ] Confirm focused tests fail for missing behavior.
- [ ] Implement scenario expansion and CSV generation.
- [ ] Run focused and complete tests.
- [ ] Run the experiment entry point and inspect generated CSV summaries.

### Task 8: Publication Figures

**Files:**
- Create: `src/amm_sim/plotting.py`
- Create: `tests/test_plotting.py`
- Create: `results/figures/.gitkeep`

- [ ] Write a failing smoke test that expects the required figure files.
- [ ] Confirm the figure test fails because plotting is absent.
- [ ] Implement focused plotting functions for slippage, IL, and LP return.
- [ ] Run the plotting test and complete suite.
- [ ] Generate figures and inspect dimensions, labels, and legends.

### Task 9: English Two-Column LaTeX Report

**Files:**
- Create: `report/main.tex`
- Create: `report/references.bib`

- [ ] Draft the report using only formulas, assumptions, generated tables, and
  generated figures from the approved scope.
- [ ] Explain why each recommended configuration was selected.
- [ ] Compile with `.conda-env/bin/tectonic report/main.tex`.
- [ ] Inspect warnings, page count, text extraction, and rendered pages.
- [x] Revise until the report is readable, compact, and naturally paginated.

### Task 10: Final Reproduction and Scope Verification

**Files:**
- Modify: `README.md`

- [x] Run the complete pytest suite with a fresh writable Matplotlib cache.
- [x] Remove generated results, re-run the experiment script, and verify all
  expected outputs regenerate.
- [x] Recompile the report from generated outputs.
- [x] Verify every base requirement and report-quality criterion against the
  design acceptance checklist.
- [x] Verify excluded extra-content features are absent.
- [x] Stop and present the completed 60+20 deliverables for user review.

## Base-Scope Completion Addendum

The final acceptance run must additionally verify:

- [x] V3 rejects exact-input swaps that exceed the single fixed range's
  capacity.
- [x] Slippage CSV output includes `net_input`.
- [x] README reproduction commands run exactly as documented.
- [x] The design and report consistently define gross-input slippage as
  including both price impact and the trading fee.
