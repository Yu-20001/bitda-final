# AMM Return Definitions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the mixed-denominator LP-return calculation with explicit
absolute and HODL-relative returns.

**Architecture:** Shared metrics calculate terminal values and both return
definitions. Deterministic and Monte Carlo experiment layers convert modeled
fee fractions to fee values, publish both measures, and use HODL-relative
excess return for comparative plots and risk statistics.

**Tech Stack:** Python 3.12, NumPy, Pandas, Matplotlib, pytest, Tectonic LaTeX.

---

### Task 1: Shared Return Metrics

**Files:**
- Modify: `tests/test_metrics.py`
- Modify: `src/amm_sim/metrics.py`

- [x] Add failing tests for terminal HODL value, absolute LP return, and excess
  return versus HODL.
- [x] Run `pytest tests/test_metrics.py -q` and confirm failure.
- [x] Implement the minimal shared value and return functions.
- [x] Run `pytest tests/test_metrics.py -q` and confirm success.

### Task 2: Deterministic and Monte Carlo Outputs

**Files:**
- Modify: `tests/test_experiments.py`
- Modify: `tests/test_monte_carlo.py`
- Modify: `src/amm_sim/experiments.py`
- Modify: `src/amm_sim/monte_carlo.py`

- [x] Add failing assertions for explicit fee values and both return columns.
- [x] Confirm focused tests fail because the columns are absent.
- [x] Generate both return definitions and base underperformance probability on excess
  return versus HODL.
- [x] Run focused tests.

### Task 3: Figures, Documentation, and Reproduction

**Files:**
- Modify: `src/amm_sim/plotting.py`
- Modify: `README.md`
- Modify: `report/main.tex`
- Modify: existing AMM design documents

- [x] Plot excess return versus HODL and update labels.
- [x] Explain both definitions and correct the fixed-seed RNG statement.
- [x] Regenerate CSVs and figures.
- [x] Compile the report and run the complete test suite.
