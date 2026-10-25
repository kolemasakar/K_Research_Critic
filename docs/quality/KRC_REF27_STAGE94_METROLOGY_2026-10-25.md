# KRC №94 — REF-27 metrological audit (2026-10-25)

Original DOI 10.2478/cons-2013-0011, uploaded original PDF SHA256: `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`.

Local stage94 Python recomputed calibration of **12 preliminary** image positions using the two original embedded Figure 1/2 rasters, and checked against stage92 stored approximations. Eight tests across stage93 and stage94 **8/8 PASS**, 0 failures. This is NOT a full KRC repository regression (last documented baseline remains 249/249).

- Figure 1 pixel axis: y 410..55 -> 3900..4900 m/s. Assumed ±5 px image-point localization -> 14.08 m/s (localization contribution only); x 104..829 -> 0..6% -> 0.0414 percentage points.
- Figure 2 pixel axis: y 77..436 -> 200..400 m/s; assumed ±5 px -> 2.79 m/s (localization only); x 103..836 -> 0..180 h -> 1.228 h. Note truncated 200-m/s vertical origin.
- Paper physical page 2 expressly reports maximum velocity/time measurement error for UK-1401 as no more than ±1%. At group dry mean UPVs from Table I this corresponds to ±40.93 (N), ±40.19 (K), ±40.11 (KV) m/s as a nominal instrument tolerance illustration, **not a probability distribution or total expanded uncertainty**.
- Do not add independent uncertainty contributions in quadrature absent established probability models and correlation information. Pixel coordinate uncertainty itself was hypothesized, not measured with repeated annotators; tick-position calibration error and curve width are unquantified. The plot/sample/group aggregation and original raw data are not identified.
- No second independent human axis reading, no experimentally validated 270-m/s/2-hour graph estimate, no complete uncertainty budget, no independently proven graph↔Table I relationship.

**Verdicts:** original source checksum PASS, local arithmetic PASS, instrument manufacturer's stated precision SOURCE_REPORTED, full scientific/figure quantitative acceptance **NO_GO**. FREE_ONLY, production, MEDIA and public access unchanged.

Next: independently adjudicate source axis and curve labels, establish data mapping where possible, preserve interpretation as unresolved otherwise; run full isolated KRC pytest and automated Critic with actual artifact identifiers.
