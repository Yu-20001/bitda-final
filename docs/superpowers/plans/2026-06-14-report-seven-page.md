# Seven-Page Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the GitHub repository link and compile the report to exactly seven readable pages.

**Architecture:** Make only small edits in the LaTeX source: add the repository URL, trim repeated prose, and reduce non-content vertical spacing only as needed. Verify the compiled PDF structurally and visually.

**Tech Stack:** LaTeX, Tectonic, Poppler PDF utilities, pytest

---

### Task 1: Add Link and Recover Space

**Files:**
- Modify: `report/main.tex`

- [ ] Add the exact public GitHub repository URL to the reproducibility section.
- [ ] Apply small spacing reductions without changing font size, margins, columns, or figure widths.
- [ ] Compile with `XDG_CACHE_HOME=../.cache HOME=.. ../.conda-env/bin/tectonic main.tex`.
- [ ] Check the page count with `pdfinfo report/main.pdf`.
- [ ] Repeat minimal adjustments until the report is exactly seven pages.

### Task 2: Verify the Final Artifact

**Files:**
- Modify: `report/main.pdf`

- [ ] Confirm extracted PDF text contains `https://github.com/Yu-20001/bitda-final`.
- [ ] Render all pages and inspect them for overflow, collisions, cramped text, and awkward whitespace.
- [ ] Run `.conda-env/bin/pytest -q`.
- [ ] Commit the LaTeX source and compiled PDF.
