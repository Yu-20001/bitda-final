# Report Figure Readability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every report figure readable by enlarging plot text and placing dense figures across both columns.

**Architecture:** Update the central plotting helper to support compact and wide figure profiles, then use LaTeX `figure*` environments for the four dense figures. Regenerate and visually verify the full report.

**Tech Stack:** Python, Matplotlib, LaTeX, Tectonic, pytest

---

### Task 1: Improve Generated Figures

**Files:**
- Modify: `src/amm_sim/plotting.py`
- Modify: `tests/test_plotting.py`
- Regenerate: `results/figures/*.pdf`

- [ ] Add compact and wide plot profiles with larger text.
- [ ] Assign dense plots to the wide profile.
- [ ] Run plotting tests and regenerate all figures.

### Task 2: Use Cross-Column Figures

**Files:**
- Modify: `report/main.tex`
- Regenerate: `report/main.pdf`

- [ ] Convert Figures 1, 4, 5, and 6 to `figure*` at full text width.
- [ ] Compile the report.
- [ ] Render and inspect every page.
- [ ] Confirm all tests pass and the repository URL remains clickable.
