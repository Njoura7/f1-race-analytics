# Backlog

Epics for members A to E. Each story has acceptance criteria and a sprint tag.

## Epic A: Data and cleaning (Member A)

- **US-A1** As a data analyst, I want the 22 circuits stored in config/circuits.yaml, so that every later step uses the same list.
  - Acceptance criteria: the list matches the FastF1 2023 schedule, and each circuit has an id and a name.
  - Sprint: S0
- **US-A2** As a data analyst, I want a loader that downloads race sessions and saves parquet snapshots, so that the rest of the team works from local files.
  - Acceptance criteria: the local cache is used, and a rerun does not download the same session twice.
  - Sprint: S1
- **US-A3** As a data analyst, I want the lap filters and outlier flags, so that only clean laps reach the models.
  - Acceptance criteria: wet, safety car, VSC, red flag, in, out and lap 1 laps are dropped, and slow laps are flagged.
  - Sprint: S1
- **US-A4** As a data analyst, I want a season split with a 2025 guard, so that the test set is protected.
  - Acceptance criteria: using 2025 without an explicit flag raises an error.
  - Sprint: S1
- **US-A5** As a data analyst, I want stable constructor ids, so that renamed teams share one id.
  - Acceptance criteria: every team name from 2023 to 2025 maps to exactly one id.
  - Sprint: S0

## Epic B: Tire degradation (Member B)

- **US-B1** As a modeller, I want the tire degradation features per stint, so that I can model stint pace.
  - Acceptance criteria: tyre age, fuel-corrected lap time and stint delta are present and documented.
  - Sprint: S1
- **US-B2** As a modeller, I want a linear slope baseline per stint, so that I have a simple reference.
  - Acceptance criteria: the slope is reported per stint and runs end to end.
  - Sprint: S1
- **US-B3** As a modeller, I want a main model with circuit and constructor effects, so that slopes fit the data better than the baseline.
  - Acceptance criteria: the model beats the baseline MAE on 2024 validation.
  - Sprint: S2
- **US-B4** As a modeller, I want slopes per compound, so that question 1 can be answered.
  - Acceptance criteria: slopes are reported per constructor and compound with an error estimate.
  - Sprint: S3

## Epic C: Pit strategy (Member C)

- **US-C1** As a strategist, I want pit loss per circuit, so that the simulator knows the cost of a stop.
  - Acceptance criteria: pit loss is reported per circuit from the in lap and out lap delta.
  - Sprint: S2
- **US-C2** As a strategist, I want safety car rates from 2023 and 2024, so that Monte Carlo uses a fair probability.
  - Acceptance criteria: 2025 is not used for the rate.
  - Sprint: S2
- **US-C3** As a strategist, I want a Monte Carlo simulator, so that I can rank candidate strategies.
  - Acceptance criteria: the simulator returns a total race time distribution per candidate.
  - Sprint: S3
- **US-C4** As a strategist, I want a comparison with the actual 2025 strategies, so that question 2 can be answered.
  - Acceptance criteria: the time delta and stop-lap agreement are reported.
  - Sprint: S4

## Epic D: Speed profiles (Member D)

- **US-D1** As an analyst, I want telemetry on a common distance grid, so that constructors can be compared fairly.
  - Acceptance criteria: every lap is resampled on the same grid step.
  - Sprint: S2
- **US-D2** As an analyst, I want corner segmentation and minimum corner speeds, so that circuit profiles can be described.
  - Acceptance criteria: corners come from the circuit info, not from manual input.
  - Sprint: S3
- **US-D3** As an analyst, I want cumulative delta time between constructors, so that speed differences are clear.
  - Acceptance criteria: the delta trace is shown per circuit.
  - Sprint: S3
- **US-D4** As an analyst, I want a constructor comparison table per circuit, so that question 3 can be answered.
  - Acceptance criteria: the table lists per-circuit summary metrics for each constructor.
  - Sprint: S4

## Epic E: Evaluation, app and tests (Member E)

- **US-E1** As an evaluator, I want metric helpers, so that scores are computed the same way everywhere.
  - Acceptance criteria: MAE, slope error and stop-lap agreement are implemented and tested.
  - Sprint: S2
- **US-E2** As an evaluator, I want validation on 2024 and a single final test on 2025, so that the split is respected.
  - Acceptance criteria: the final test only runs with the explicit flag.
  - Sprint: S4
- **US-E3** As a developer, I want placeholder tests and a CI workflow, so that changes do not break the repo.
  - Acceptance criteria: ruff and pytest run cleanly in CI.
  - Sprint: S1
- **US-E4** As a presenter, I want a Streamlit app with three tabs, so that results can be shown live.
  - Acceptance criteria: the app starts and shows the three result tabs.
  - Sprint: S4

## Cross-track dependencies

- B and D depend on A for clean laps, telemetry and the season split.
- C depends on B for the degradation model.
- E depends on A, B, C and D for results to evaluate and show.
- The final 2025 test depends on B, C and D being frozen after validation.
