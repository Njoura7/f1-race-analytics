
# F1 Telemetry and Race Analytics

A Data Science Club (ELTE) project. We study official Formula 1 race data from
three seasons and compare how different constructors manage tyres, pit stops and
raw speed. This repo is the shared starting point: it holds the plan, the rules
and a skeleton of stub files. The team writes the actual analysis code.

## Goal

Build and evaluate constructor-level models of tire degradation and pit
strategy, plus a speed profile comparison, on official F1 race data, training on
2023 and 2024 and testing on 2025. The project answers three questions:

1. How quickly do tyres lose pace for each constructor and compound?
2. Given that, which pit strategy would minimise race time, and how close was it to what teams actually did in 2025?
3. How do constructors differ in speed profile at the same circuit?

Final deliverables: four short notebooks, one evaluation table (validation 2024,
final test 2025), a Streamlit app, and `docs/study_notes.md`.

## Scope and assumptions

1. Official races only: the main Grand Prix race session (FastF1 session type "R") of each official championship round, which counts for championship points. Practice, qualifying and sprint sessions are excluded, because sprints are shorter and use fuel and tyres differently.
2. Seasons: 2023 (22 rounds), 2024 and 2025 (24 rounds each). To compare like for like we use the 22 circuits that were official rounds in all three seasons, which are the 2023 calendar. The extra 2024 and 2025 rounds (China and Imola) are left out by default and can be added with a config flag (`include_extra_rounds`). Member A verifies the list against the FastF1 event schedule and stores it in `config/circuits.yaml`.
3. Constructors, not drivers: line-ups change between seasons, so we model at constructor level and treat drivers as noise. `config/constructors.yaml` maps renamed teams to one stable id (for example Alfa Romeo to Sauber, AlphaTauri to RB to Racing Bulls).
4. Time-based split: train 2023, validate 2024 (development and tuning), final test 2025 used once at the end. 2026 is excluded because of new regulations. 2025 must not be used for tuning.
5. We compare mechanisms (degradation per compound, pit timing, strategy choices, speed profiles), not absolute team pace, because car performance changes every year.
6. Data comes from FastF1 with a local cache. Lap data is loaded for all in-scope races. Telemetry is loaded only for the speed profile track, for 3 chosen circuits, fastest laps only.

## Team

| Name | Role |
| --- | --- |
| Aziz Najjar | Lead: product owner and Scrum master |
| Bouderhem Fares, Temirova Jazeera | Data and cleaning (pair) |
| Grigoryan Hayk, Nayan Saidul Islam | Tire degradation (pair) |
| Cupi Olivares Jair Alessandro | Pit strategy (depends on tire degradation) |
| Petro Waseem | Speed profiles |
| Jahiu Erblina | Evaluation, app and tests |

Time budget: 6 weeks, about 2 to 3 hours per member per week, roughly 8 hours
per member in total. Tasks are small. Anything extra is marked STRETCH.

## Workflow steps

1. Scope: fix circuits, seasons and constructors in `config/`.
2. Load: download race laps, weather and track status with FastF1 and save parquet snapshots in `data/`.
3. Clean: keep accurate laps only; drop wet laps, safety car and VSC laps, red flag laps, in and out laps and lap 1; flag outlier laps (for example slower than 107 percent of the stint median); handle missing lap times; map constructors to stable ids.
4. Feature engineering: build features per track (see below).
5. Split: season-based train, validation and test, with a guard so 2025 is only used with an explicit flag.
6. Model: baseline first, then the main model, per track.
7. Evaluate: validate on 2024, then run the final test on 2025 once.
8. Present: results table, plots and the Streamlit app.

See `docs/architecture.md` for the workflow diagram.

## Feature engineering

- Tire degradation: tyre age in laps, stint number, compound, fuel-corrected lap time (lap number as a fuel burn proxy), lap time delta to the first clean lap of the stint, track and air temperature, circuit id, constructor id. Target: fuel-corrected lap time or the delta above.
- Pit strategy: pit loss per circuit (in lap plus out lap versus clean laps), stint lengths, number of stops, compound sequence, safety car rate per circuit from 2023 and 2024.
- Speed profiles: telemetry resampled on a common distance grid, speed, throttle and brake traces, minimum speed per corner, top speed, full throttle share, cumulative delta time between constructors.

## Modelling approach

1. Tire degradation. Baseline: linear slope per stint. Main model: gradient boosting or linear regression with circuit, compound and constructor features. STRETCH: mixed-effects model. Metric: MAE of predicted stint pace and slope error, on validation then on 2025.
2. Pit strategy. Deterministic simulator of total race time for one-stop and two-stop strategies using the degradation model and pit loss per circuit. STRETCH: Monte Carlo with safety car probability. Compare the recommended strategy with what teams actually ran in 2025. Metric: time delta and stop-lap agreement.
3. Speed profiles. Descriptive: constructor comparison at 3 circuits (delta time, corner minimum speeds, top speed). STRETCH: circuit similarity.

## Tools and technologies

| Tool | Why |
| --- | --- |
| FastF1 | Official timing, lap and telemetry data from a free open source API |
| pandas | Tabular cleaning, filtering and joins |
| scikit-learn | Baselines and gradient boosting models |
| statsmodels | Optional mixed-effects models for degradation |
| Plotly | Interactive charts for notebooks and the app |
| Streamlit | Quick web app for the results |

## Project structure

```text
f1-race-analytics/
  README.md                     # project overview, goal, scope, workflow and how to run
  CONTRIBUTING.md               # how members contribute, branch and review rules
  requirements.txt              # pinned Python dependencies
  Makefile                      # common tasks (setup, lint, test, app)
  .gitignore                    # files and folders kept out of git
  config/
    settings.yaml               # shared settings for seasons, paths, thresholds and the extra rounds flag
    circuits.yaml               # the 22 circuits used in the project
    constructors.yaml           # stable constructor ids and team renames
  data/
    README.md                   # a 3 line note that data files are local and gitignored
    .gitkeep                    # keeps the empty data folder in git
  notebooks/
    01_eda.ipynb                # explore coverage and lap data quality
    02_tire_degradation.ipynb   # fit and check tire degradation models
    03_pit_strategy.ipynb       # simulate and compare pit strategies
    04_speed_profiles.ipynb     # compare constructor speed profiles
  src/
    data/
      loader.py                 # downloads race laps, weather and track status, and saves parquet snapshots
      cleaning.py               # applies the lap filters and outlier flags
      split.py                  # splits data by season with a 2025 test guard
    features/
      tire_features.py          # builds tire degradation features per stint
      strategy_features.py      # builds pit strategy features per circuit
      telemetry_features.py     # builds speed profile features on a distance grid
    models/
      tire_degradation.py       # fits the tire degradation baseline and main model
    strategy/
      simulator.py              # simulates race time for one-stop and two-stop pit strategies
    telemetry/
      speed_profile.py          # compares constructor speed profiles per circuit
    evaluation/
      metrics.py                # metric helpers for pace and strategy evaluation
      backtest.py               # runs validation on 2024 and the final test on 2025
  models/
    .gitkeep                    # keeps the empty models folder in git
  app/
    app.py                      # Streamlit skeleton with sidebar filters and three tabs
  tests/
    test_split.py               # placeholder tests for the season split guard
    test_cleaning.py            # placeholder tests for the lap filters
    test_constructors.py        # placeholder tests for the constructor mapping
  docs/
    architecture.md             # workflow diagram and data flow notes
    SCRUM.md                    # roles, cadence, definition of done and sprint goals
    backlog.md                  # task table with owners, hours, sprints and acceptance criteria
    status.md                   # weekly update log kept by the lead
    study_notes.md              # study notes and references per member
    presentation_outline.md     # outline for the 10 minute club talk
    images/
      .gitkeep                  # keeps the empty images folder in git
  .github/
    workflows/ci.yml            # continuous integration with ruff and pytest
    ISSUE_TEMPLATE/user_story.md  # issue template matching the backlog task table
    pull_request_template.md    # pull request checklist template
```

## How to run

```bash
make setup    # create .venv and install requirements
make lint     # run ruff
make test     # run pytest
make app      # start the Streamlit app
```

Run the notebooks in order: `01_eda`, `02_tire_degradation`, `03_pit_strategy`,
`04_speed_profiles`. The 2025 test split only runs with an explicit flag.

## Results

Placeholder. The evaluation table and plots are filled in at the end of the
project. Nothing is invented here.

## Key learnings

Placeholder. The team fills this in after the final presentation.


