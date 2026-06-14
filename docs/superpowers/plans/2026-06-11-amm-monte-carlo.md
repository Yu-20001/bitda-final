# AMM Monte Carlo Risk Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reproducible Monte Carlo extension that compares LP-return
distributions and V3 fixed-range risk across volatile-asset AMMs.

**Architecture:** Keep GBM path generation and per-configuration aggregation in
one focused Monte Carlo module. Reuse existing position valuation and metric
functions, then extend the experiment runner, plotting layer, README, and
report with compact generated evidence.

**Tech Stack:** Python 3.12, NumPy, Pandas, Matplotlib, pytest, Tectonic LaTeX.

---

### Task 1: Monte Carlo Path Generator

**Files:**
- Create: `src/amm_sim/monte_carlo.py`
- Create: `tests/test_monte_carlo.py`

- [x] Write failing tests for fixed-seed determinism, dimensions, and zero
  volatility.
- [x] Run focused tests and confirm they fail because the module is absent.
- [x] Implement the minimal vectorized GBM path generator.
- [x] Run focused tests and the complete suite.

### Task 2: Monte Carlo Summary Metrics

**Files:**
- Modify: `src/amm_sim/monte_carlo.py`
- Modify: `tests/test_monte_carlo.py`

- [x] Write failing tests for zero-volatility summaries, required columns, and
  V3 path availability.
- [x] Confirm focused tests fail for missing summary behavior.
- [x] Implement per-path IL, fee return, absolute LP return, HODL-relative
  excess return, and compact summaries for the approved six configurations.
- [x] Run focused tests and the complete suite.

### Task 3: Scenario and Experiment Integration

**Files:**
- Modify: `config/scenarios.yaml`
- Modify: `src/amm_sim/experiments.py`
- Modify: `tests/test_experiments.py`

- [x] Write failing tests for approved Monte Carlo settings, 18 summary rows,
  required columns, no missing values, and deterministic generation.
- [x] Confirm focused tests fail.
- [x] Add approved settings and generate `monte_carlo_summary.csv`.
- [x] Run focused tests and the complete suite.

### Task 4: Monte Carlo Figures

**Files:**
- Modify: `src/amm_sim/plotting.py`
- Modify: `tests/test_plotting.py`

- [x] Extend the figure smoke test to require return-risk and V3 range-risk
  figures, then confirm failure.
- [x] Implement the two focused publication figures.
- [x] Run plotting tests and inspect rendered figures.

### Task 5: Report and Reproduction Documentation

**Files:**
- Modify: `README.md`
- Modify: `report/main.tex`
- Modify: `docs/superpowers/plans/2026-06-11-amm-monte-carlo.md`

- [x] Document Monte Carlo assumptions, exclusions, outputs, and reproduction.
- [x] Add a dedicated report chapter using only generated evidence.
- [x] Explain every recommended parameter choice and limitation.
- [x] Reproduce all CSVs and figures from the documented command.
- [x] Compile and visually inspect the naturally paginated report.
- [x] Run the complete test suite and final acceptance checks.
