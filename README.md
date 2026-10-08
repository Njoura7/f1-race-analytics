# F1 Telemetry and Race Analytics

A Data Science Club (ELTE) project. We study Formula 1 race data from three
seasons and compare how different constructors manage tyres, pit stops and raw
speed. This repo is the shared starting point: it holds the plan, the rules and
a skeleton of stub files. The team writes the actual analysis code.

## Goal

Build and evaluate constructor-level models of tire degradation and pit
strategy, plus a speed profile comparison, on F1 race data from 22 circuits,
training on 2023 and 2024 and testing on 2025. The project answers three
questions:

1. How quickly do tyres lose pace for each constructor and compound?
2. Given that, which pit strategy would minimise race time, and how close was it to what teams actually did in 2025?
3. How do constructors differ in speed profile at the same circuit?

Final deliverables: four analysis notebooks, an evaluation table (validation
2024 and final test 2025), and a Streamlit app.

## Scope and assumptions

1. Circuits: only the 22 circuits that appear in all of the 2023, 2024 and 2025 seasons (the 2023 calendar). Member A confirms the list against the FastF1 event schedule and stores it in `config/circuits.yaml`.
2. Constructors, not drivers: line-ups change between seasons, so we model at constructor level and treat drivers as noise. `config/constructors.yaml` maps renamed teams to one stable id (for example Alfa Romeo to Sauber, AlphaTauri to RB to Racing Bulls).
3. Time-based split: train on 2023, validate on 2024 (development and tuning), final test on 2025, used once at the end. 2026 is excluded because of new regulations. 2025 must not be used for tuning.
4. We compare mechanisms (degradation per compound, pit timing, strategy choices, speed profiles), not absolute team pace, because car performance changes every year.
5. Data comes from FastF1 (open source API) with a local cache. Light cleaning is part of the project (see workflow step 3).

## Team

| Name | Role |
| --- | --- |
| Lead name | Team Lead: product owner and Scrum master, no coding tasks |
| Member A | Data and cleaning |
| Member B | Tire degradation |
| Member C | Pit strategy (depends on B) |
| Member D | Speed profiles |
| Member E | Evaluation, app and tests |

## Workflow steps

1. Scope: fix circuits, seasons and constructors in `config/`.
2. Load: download race sessions with FastF1 using the local cache, save to parquet snapshots in `data/`.
3. Clean: keep accurate laps only; drop wet laps, safety car and VSC laps, red flag laps, in and out laps and lap 1; flag outlier laps (for example slower than 107 percent of the stint median); handle missing lap times; map constructors to stable ids; join weather and track status.
4. Feature engineering: build features per track (see below).
5. Split: season-based train, validation and test, with a guard so 2025 is only used with an explicit flag.
6. Model: baselines first, then the main model, per track.
7. Evaluate: validate on 2024, then run the final test on 2025 once.
8. Present: results table, plots and the Streamlit app.

See `docs/architecture.md` for the workflow diagram.

## Feature engineering

- Tire degradation: tyre age in laps, stint number, compound (and C-number when available), fuel-corrected lap time (lap number as a fuel burn proxy), lap time delta to the first clean lap of the stint, track temperature, air temperature, circuit id, constructor id, traffic proxy (gap to the car ahead). Target: fuel-corrected lap time or the delta above.
- Pit strategy: pit loss per circuit (in lap plus out lap delta versus clean laps), stint lengths, number of stops, compound sequence, safety car rate per circuit from 2023 and 2024, undercut window estimates.
- Speed profiles: telemetry resampled on a common distance grid, speed, throttle and brake traces, corner segmentation from the circuit info, minimum speed per corner, top speed, full throttle share, braking points, cumulative delta time between constructors.

## Modelling approach

1. Tire degradation. Baseline: linear slope per stint. Main model: mixed-effects or gradient boosting with circuit and constructor effects. Metric: MAE of predicted stint pace and slope error, on validation then on 2025.
2. Pit strategy. Simulate total race time from the degradation model, pit loss per circuit and safety car probability (Monte Carlo). Compare the recommended strategy with the strategies actually run in 2025. Metric: time delta and stop-lap agreement.
3. Speed profiles. Mostly descriptive: constructor comparisons per circuit and circuit similarity. Metric: agreement between the descriptive findings and known car characteristics, plus delta time summaries.

## Tools and technologies

| Tool | Why |
| --- | --- |
| FastF1 | Official timing, lap and telemetry data from a free open source API |
| pandas | Tabular cleaning, filtering and joins |
| scikit-learn | Baselines and gradient boosting models |
| statsmodels | Mixed-effects models for degradation |
| Plotly | Interactive charts for notebooks and the app |
| Streamlit | Quick web app for the results |

## Project structure

```text
f1-race-analytics/
  README.md                 # project overview, goal, scope, workflow and how to run
  CONTRIBUTING.md           # how members contribute, branch and review rules
  requirements.txt          # pinned Python dependencies
  Makefile                  # common tasks (setup, lint, test, app)
  .gitignore                # files and folders kept out of git
  config/                   # settings and reference data
    settings.yaml           # shared settings for seasons, paths and thresholds
    circuits.yaml           # the 22 circuits used in the project
    constructors.yaml       # stable constructor ids and team renames
  data/                     # local parquet snapshots (gitignored)
  notebooks/                # one notebook per analysis track
    01_eda.ipynb            # explore coverage and lap data quality
    02_tire_degradation.ipynb  # fit and check tire degradation models
    03_pit_strategy.ipynb   # simulate and compare pit strategies
    04_speed_profiles.ipynb # compare constructor speed profiles
  src/
    data/
      loader.py             # downloads FastF1 sessions and saves parquet snapshots
      cleaning.py           # applies the lap filters and outlier flags
      split.py              # splits data by season with a 2025 test guard
    features/
      tire_features.py      # builds tire degradation features per stint
      strategy_features.py  # builds pit strategy features per circuit
      telemetry_features.py # builds speed profile features on a distance grid
    models/
      tire_degradation.py   # fits the tire degradation baseline and main model
    strategy/
      simulator.py          # simulates race time for candidate pit strategies
    telemetry/
      speed_profile.py      # compares constructor speed profiles per circuit
    evaluation/
      metrics.py            # metric helpers for pace and strategy evaluation
      backtest.py           # runs validation on 2024 and the final test on 2025
  models/                   # saved model artifacts (gitignored)
  app/
    app.py                  # Streamlit skeleton with sidebar filters and three tabs
  tests/
    test_split.py           # placeholder tests for the season split guard
    test_cleaning.py        # placeholder tests for the lap filters
    test_constructors.py    # placeholder tests for the constructor mapping
  docs/
    architecture.md         # workflow diagram and data flow notes
    SCRUM.md                # roles, cadence, definition of done and sprint goals
    backlog.md              # epics and user stories for members A to E
    presentation_outline.md # outline for the 10 minute club talk
    images/                 # images used in docs and the presentation
  .github/
    workflows/ci.yml        # continuous integration with ruff and pytest
    ISSUE_TEMPLATE/user_story.md  # issue template for user stories
    pull_request_template.md     # pull request checklist template
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
