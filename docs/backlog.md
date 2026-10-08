# Backlog

Three one-week sprints. Each task has an owner, a type, hours, a sprint, a
deliverable and acceptance criteria. STRETCH items are optional and extra.

| ID | Owner (pair) | Type | Hours | Sprint | Deliverable | Acceptance criteria |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | All | Apply | 0.5 each | 1 | Kickoff, read the README, agree on scope, split and function interfaces | Each member has confirmed their tasks |
| T2 | A | Study and Apply | 2 | 1 | Load and cache race laps, weather and track status for all in-scope races 2023 to 2025 into parquet; verify circuits.yaml against the FastF1 schedule | A coverage note lists races loaded and missing |
| T3 | B | Study | 2 | 1 | Study tyre degradation (fuel effect, compound, track evolution), a 10 line method note on fuel correction, 2 references in study_notes.md | Method note and references added |
| T4 | C | Study | 2 | 1 | Study pit loss and undercut basics, a method note on estimating pit loss per circuit, simulator inputs and outputs defined | Note added and interfaces agreed |
| T5 | D | Study and Apply | 2 | 1 | Study FastF1 telemetry and circuit info, choose 3 circuits, load fastest 2024 race laps, plot speed against distance for two constructors | Plot shown in notebook 04 |
| T6 | E | Study and Apply | 2 | 1 | Define metrics and naive baselines (previous season average per constructor and circuit), write the 2025 split guard and its test, set up CI | Guard test passes and CI runs |
| T7 | A + B (pair) | Apply | 3 each | 2 | Cleaning filters and the stint table with tyre age and fuel-corrected lap time | Notebook 01 shows before and after counts and a stint plot |
| T8 | B | Apply | 2 | 2 | Baseline slope per stint and main model v1, trained on 2023, validated on 2024 | Notebook 02 shows the metric table |
| T9 | B + C (pair) | Apply | 2 each | 2 | A degradation function (compound, tyre age, circuit, constructor) the simulator can call; C estimates pit loss per circuit | Function is importable and the pit loss table is ready |
| T10 | C | Apply | 1.5 | 2 | Simple deterministic simulator for one-stop and two-stop strategies at one circuit | Simulator returns total times for both strategies |
| T11 | D | Apply | 3 | 2 | Constructor speed profile comparison at the 3 circuits (delta time, corner minimum speeds, top speed) | Notebook 04 shows the comparison |
| T12 | E | Apply | 3 | 2 | Metrics and backtest functions plus the app skeleton wired to saved outputs | App starts and shows the three tabs |
| T13 | B + E (pair) | Apply | 1.5 each | 3 | Final run on 2025, once, and the results table | The table is in the README |
| T14 | C | Apply | 2 | 3 | Compare recommended strategies with the actual 2025 strategies at the 3 circuits | Comparison table in notebook 03 |
| T15 | D + E (pair) | Apply | 1.5 each | 3 | Finish the speed profile and strategy tabs in the app | Both tabs show results |
| T16 | A | Apply | 1.5 | 3 | Tests for cleaning and constructors, README How to run check on a fresh clone | Tests pass and the steps are verified |
| T17 | Lead with all | Apply | 2 | 3 | Results and key learnings in the README, presentation rehearsal using docs/presentation_outline.md | README updated and rehearsal done |

## STRETCH (not required)

- Monte Carlo with safety car probability.
- Mixed-effects degradation model.
- Circuit similarity.
- Extra rounds (China and Imola).

## Member load

Kickoff T1 is included. STRETCH items are excluded.

| Member | Hours |
| --- | --- |
| Lead | 2.5 |
| A | 7 |
| B | 11 |
| C | 8 |
| D | 7 |
| E | 8.5 |

B and E are above the 8 hour target. To bring them down, the lead can move B's
study note (T3) into T8 and split each pair task so that one owner leads and the
other only reviews.
