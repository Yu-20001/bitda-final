# Report Figure Readability Design

## Goal

Improve the readability of Figures 1--7 without constraining the report to
seven pages.

## Layout

Figures 1, 4, 5, and 6 contain many series or dense legends and will span both
text columns. Figures 2, 3, and 7 contain fewer series and will remain
single-column figures. The surrounding report structure, typography, margins,
and table layouts remain unchanged.

## Figure Styling

All generated figures will use larger axis labels, tick labels, and legends.
The plotting code will use a wider canvas for dense figures and a compact
canvas for simple figures so text remains legible at its final printed width.
Labels may be shortened only where their meaning remains unambiguous.

## Verification

- Regenerate all CSV outputs and PDF figures with the documented experiment
  command.
- Run the automated test suite.
- Compile the report with Tectonic.
- Render and inspect every report page for readable plot text, reasonable
  float placement, overflow, and collisions.
- Confirm the repository URL remains present and clickable.
