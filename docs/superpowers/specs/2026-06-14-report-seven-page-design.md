# Seven-Page Report Design

## Goal

Add the public GitHub repository URL to the report and reduce the compiled
report from eight pages to exactly seven without materially changing its
visual layout.

## Approach

Keep the existing A4, 11-point, two-column layout, margins, figure widths, and
content structure. Add the repository URL at the end of the reproducibility
section. Recover the small amount of space needed to move the final
bibliography entry from page eight onto page seven by:

1. Removing repeated or nonessential wording where it does not change a claim.
2. Applying small, document-wide reductions to heading, float, list, and
   bibliography spacing only if textual trimming is insufficient.
3. Avoiding font-size reductions, margin changes, figure resizing, and major
   float relocation.

## Verification

- Compile `report/main.tex` with Tectonic.
- Confirm `report/main.pdf` contains the exact repository URL:
  `https://github.com/Yu-20001/bitda-final`.
- Confirm the compiled PDF contains exactly seven pages.
- Render and visually inspect all seven pages for overflow, collisions,
  awkward whitespace, and noticeably cramped text.
- Run the existing automated test suite to ensure the reproducible project
  remains intact.
