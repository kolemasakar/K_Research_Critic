# KRC №85 — REF-27 figure axis calibration gate, 2026-10-25

## Owner-approved scope
Implement reproducible plot digitization readiness for REF-27 Fig. 1/2 without asserting nonexistent figure data. FREE_ONLY; isolated read-only research host tests; no production, MEDIA, public distribution or external scientific peer review.

## Source
Lencis/Udris/Korjakins 2013, DOI 10.2478/cons-2013-0011, RTU institutional PDF https://ortus.rtu.lv/science/en/publications/16677/fulltext.
Original PDF sha256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`. Figures 1/2 at physical PDF page 4.
The page contains two embedded PDF image objects according to pypdf. Extraction of their actual raster geometry on isolated host could not be completed because the local pypdf image helper needs Pillow, not currently installed in the test venv. Thus no verified image width/height, axis ticks, curve pixels or raw figure-coordinate series were obtained. Do NOT substitute guessed axis marks, simulated points or screenshot-derived values.

## Implemented
- `src/krc_research/figure_axis_calibration.py` defines an **explicit conditional affine calibration** requiring source file sha256, physical page, figure identifier, image pixel width/height, *two distinct human-verified tick locations and values for each x/y axis*, consistent unit per axis and declared pixel-coordinate uncertainty.
- Calibrated x/y values are computed from tick coordinates only; the returned local upper uncertainty contributions are `abs(axis_unit_per_pixel) * pixel_uncertainty`. This is a **pixel-position bound**, NOT total scientific measurement uncertainty.
- Blocked verdict `BLOCKED_UNVERIFIED_AXIS_TICKS` when axis ticks are not verified, even if a user supplies nominal point pixels.
- Always `scientific_plot_points_verified=False` and `publication_ready=False`. Geometry alone cannot certify figure correctness.
- `tests/test_p0_figure_axis_calibration.py`: six synthetic geometric/negative controls incl. reversed image-y-to-plot-y coordinates, uncertainty bound, unit mismatch, out-of-raster point, degenerate ticks and bad PDF hash.

## Real REF-27 figure admission tests
Ran both FIG1 and FIG2 against source SHA on isolated krc-cobalt with `inspector_verified_ticks=False`. Both yielded `BLOCKED_UNVERIFIED_AXIS_TICKS` and `scientific_plot_points_verified=False`. Dimensions in this test are **placeholders used only to exercise blocking**, not actual measured figure pixels; expressly NOT a digitization of the original charts.
Isolated evidence file `/tmp/krc-ext-s04-acceptance/figures_calibration_gate_20261025.json`.

## Regression
`PYTHONPATH=src .venv/bin/python -m pytest -q tests/` on isolated `krc-cobalt` → **249 passed / 0 failed** (1.70s), previous baseline 243.

## Critic verdict and limitations
- Geometric calibration engine engineering: PASS (synthetic tests).
- Original source PDF raster inspection/dimension measurement: SHORTFALL.
- Fig1/2 axis tick identity, value mapping, panel dimensions, pixel plots: SHORTFALL.
- Published graph/table quantitative correspondence: **NO_GO / unverified**.
- Independent scientific peer review and publication authorization: NO_GO, as agreed until final stage.
- Extracted words and captions from original REF-27 alone are not sufficient to validate plotted data.

## Next technical work
Obtain actual figure raster images from the source PDF within an approved isolated research directory (e.g. install Pillow in isolated test venv only if allowed under FREE_ONLY, otherwise use available local renderer). Inspect axis tick labels and figure geometry, record real tick pixel coordinates with verified citation. Only then run calibrated points with declared extraction uncertainty and reconcile individual Fig1/2 series versus Table I. Preserve the image/axis uncertainty in the evidence ledger.

## Same-turn follow-up: genuine raster extraction completed
After initial assessment, Pillow was successfully installed **only inside** the isolated `/tmp/krc-p0-offline-20261025/.venv` (no production changes). Embedded image extraction succeeded. Update prior technical blocker as **RESOLVED**: it is now possible to obtain the actual raster assets.

New `src/krc_research/figure_asset_inventory.py` and four negative/positive tests in `tests/test_p0_figure_asset_inventory.py`; original RTU PDF physical page 4 inventory produced:
- Embedded image 1 (`Im3.png`, visually Figure 1): **865 × 526 px**, 32,630 bytes; extracted RGB PNG SHA256 `c8a05c4cca3dd55d260793f7728606703078406c77b253e774e1a11211750b18`.
- Embedded image 2 (`Im4.png`, visually Figure 2): **865 × 487 px**, 32,044 bytes; extracted RGB PNG SHA256 `8e83be3ff8223df0910b8341d04e03b9fab3d05aa5696fe963b825c0c226d9f9`.

Both original raster figures were inspected: Fig.1 visibly plots UPV (m/s) versus weight-based water absorption (0–6% axis), showing groups N/K/Kv; Fig.2 plots a decreasing UPV quantity (m/s) against elapsed time (0–180h), with visually reversed vertical axis (200 at top; 400 at bottom). These are **descriptions of the actual figure labels**, not a calibrated verification of curve coordinates.

Both image files were retained **only in isolated scratch directory** `/tmp/krc-ext-s04-acceptance/`, with inventory receipt `ref27_real_figures_inventory_20261025.json`. These are not committed to GitHub; preserve accepted data retention policy.

**Revised engineering test result: 253/253 PASS, 0 failures (2.86s)**. Figure assets extracted = PASS; axes tick values and pixel locations independently verified = NOT YET; line-curve numeric digitization = SHORTFALL; scientific experiment validation = NO_GO. Prior provisional `image_width=100` gate tests were synthetic and must not be reused as actual source dimensions. Calibration must use real 865-pixel widths and independently documented axis ticks.
