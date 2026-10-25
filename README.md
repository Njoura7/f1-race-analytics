# F1 Telemetry and Race Analytics

A Data Science Club (ELTE) project. We study official Formula 1 race data from three seasons and compare how different constructors manage tyres, pit stops and raw speed. This repo holds the plan, the rules and a skeleton of stub files. The team writes the actual analysis code.

> ## Update, 25 October 2026: new team structure. Please read this first.
>
> One of our teammates has exams and has to step back from the project for now. We thank them for the early work. To keep everyone working in pairs, and to stop people waiting for each other, we changed three things:
>
> 1. **Three pairs** instead of five separate workstreams (see [Team](#team)).
> 2. **A seed data table**, so the tyre and pit pair can start without waiting for the cleaning (see [Who waits for whom](#who-waits-for-whom)).
> 3. **A shorter plan with a fixed end:** everything is done by **the end of November at the latest** (see [Plan](#plan)).
>
> **What you do now**
> 1. Find your pair in the [Team](#team) table and check that your GitHub username is correct.
> 2. Make sure you can open this repo. If you cannot, accept the invitation from GitHub (check your email, invitations expire after 7 days) and tell Aziz so he can send a new one.
> 3. When your issues appear, open each one and fill in three things: a short **description**, your own **estimate in hours**, and your **plan or suggestions**. Our estimates are only a starting point.
> 4. Do your Phase 1 issue. This week is light: about **2 to 4 hours per person**.
> 5. Come to the short sync on **Wednesday or Thursday** (the day is confirmed in the group chat).

## Goal

Build and evaluate constructor-level models of tyre degradation and pit strategy, plus a speed profile comparison, on official F1 race data. We train on 2023, validate on 2024 and test on 2025 once. The project answers three questions:

1. How quickly do tyres lose pace for each constructor and compound?
2. Given that, which pit strategy would minimise race time, and how close was it to what teams actually did in 2025?
3. How do constructors differ in speed profile at the same circuit?

Final deliverables: four short notebooks, one evaluation table (validation 2024, final test 2025), a Streamlit app, and `docs/study_notes.md`.

## Scope and assumptions

- **Official races only:** the main Grand Prix race session (FastF1 session type "R") of each official championship round, which counts for championship points. Practice, qualifying and sprint sessions are excluded, because sprints are shorter and use fuel and tyres differently.
- **Seasons:** 2023 (22 rounds), 2024 and 2025 (24 rounds each). To compare like for like we use the **22 circuits that were official rounds in all three seasons**, which are the 2023 calendar. The extra 2024 and 2025 rounds (China and Imola) are left out by default and can be added with a config flag (`include_extra_rounds`). The data pair verifies the list against the FastF1 event schedule and stores it in `config/circuits.yaml`.
- **Constructors, not drivers:** line-ups change between seasons, so we model at constructor level and treat drivers as noise. `config/constructors.yaml` maps renamed teams to one stable id (for example Alfa Romeo to Sauber, AlphaTauri to RB to Racing Bulls).
- **Time-based split:** train on 2023, validate on 2024 (development and tuning), final test on 2025, used once at the end. 2026 is excluded because of new regulations. 2025 must not be used for tuning.
- We compare **mechanisms** (degradation per compound, pit timing, strategy choices, speed profiles), not absolute team pace, because car performance changes every year.
- Data comes from FastF1 with a local cache. Lap data is loaded for all in-scope races. Telemetry is loaded only for the speed profile track, for 3 chosen circuits, fastest laps only.

## Team

We work in **three pairs**. Every task has a main owner and a second person, a partner or a reviewer. One drives and one navigates, and you swap halfway through a task. Hayk and Waseem are in different pairs on purpose, so the F1 and data science knowledge is spread across the team.

| Pair | Members | GitHub | Owns |
|---|---|---|---|
| Lead | Aziz Najjar | Njoura7 | Product owner and Scrum master. Seed table, data contract, board, weekly sync |
| **1. Data foundation** | Bouderhem Fares | feres2005 | Loading, cleaning, constructor mapping, data tests |
| | Temirova Jazeera | jazeerabt | |
| **2. Tyres and pit** | Grigoryan Hayk | pyKi11er | Tyre degradation model, then the pit strategy simulator |
| | Cupi Olivares Jair Alessandro | Alessandro9102 | |
| **3. Speed and evaluation** | Petro Waseem | waseempt | Speed profiles, metrics, the 2025 split guard, CI, backtest, app |
| | Jahiu Erblina | erblinajahiu | |

Time budget: about 2 to 3 hours per member per week, roughly 12 to 15 hours per member in total, light while exams last. Tasks are small. Anything extra is marked STRETCH.

## Who waits for whom

We want to be honest about this, because it is the main risk of the project. Almost everything needs clean data, and the data pair is on the critical path.

| Who | Needs | What blocks them | What we do about it |
|---|---|---|---|
| Data pair | FastF1 and the circuit and constructor lists | Nothing | Cleaning is delivered in two steps, small v0 first |
| Tyres (Hayk, Jair) | Clean lap table | **Yes, until the seed table or cleaning v0 exists** | Aziz publishes a seed table first. Until then, the study tasks (T1, P1) |
| Pit (Jair) | Clean laps for pit loss, and a degradation function from tyres | **Yes, on cleaning and partly on tyres** | The simulator starts with the tyre baseline slope, and the main model replaces it later |
| Speed (Waseem) | Its own telemetry for 3 circuits, fastest laps, and the constructor ids | **Not on the lap cleaning.** It loads telemetry directly with FastF1 | Starts now |
| Evaluation (Erblina) | Metric definitions at first. Model outputs later | **Not at the start. Yes later:** the backtest and the final run need the tyre and pit results | Metrics, split guard and CI first |

The risk: if the seed table is late, tyres and pit are blocked. If cleaning v1 is late, the final run on 2025 is late. If you are blocked, add the `blocked` label to your issue, write what you wait for, and tell Aziz in the chat the same day.

### The seed table and the cleaning, in three steps

1. **Seed (Aziz, first).** A table of 2023 laps for all 22 circuits, exported from Aziz's own data pipeline and saved as `data/seed/laps_2023_v0.parquet`. It is version v0, so small differences from our own cleaning are expected.
2. **Cleaning v0 (data pair).** Reproduce the seed with the repo's own code, using the same columns. Filters are **flags, not deletes**, so we can change a rule later without breaking the models. A test compares the result with the seed.
3. **Cleaning v1 (data pair).** Add 2024 and 2025, the 107 percent flag, an outlier rule and tests. When the repo's output matches the seed, the repo's file replaces it and the seed is deleted (task D7).

Anything that the three tracks do not need goes to the backlog.

### Data contract, the columns of the lap table

| Column | Meaning |
|---|---|
| `season`, `round`, `circuit_id` | Which race |
| `constructor_id` | Stable team id |
| `driver_code` | Only for joins, never a feature |
| `lap_number`, `stint`, `compound`, `tyre_life` | Tyre context |
| `lap_time_s` | Lap time in seconds |
| `is_in_lap`, `is_out_lap`, `is_lap_one` | Pit and start flags |
| `track_status_flag`, `is_wet` | Safety car, VSC, red flag and wet, as flags |
| `is_valid` | The cleaning verdict |

This table is also kept in `docs/data_contract.md`.

## Plan

The end date is fixed: **everything is done by the end of November at the latest**, including the final run on 2025, the README results and the club talk. We do not use week numbers, because the time left is short and dates would be misleading. We work in four phases, in order. Aziz and the team agree on the dates of each phase in the weekly sync.

| Phase | Goal | Main issues |
|---|---|---|
| 1. Start (this week, light) | Everyone is set up. Seed table and data contract exist. Cleaning v0 loader starts. Study tasks | K1, D0, D0b, D3a, T1, P1, S1, E1 |
| 2. Build | Cleaning v0 done. Features. Tyre baseline and first main model. Pit loss. Speed distance grid and comparison. CI | D4a, D2, D3b, D5, T2, T3, T4a, P2, S2, S3, E2 |
| 3. Connect | Cleaning v1 done and the seed retired. Main tyre model tuned. Degradation function. Pit simulator. Backtest and app skeleton | D4b, D7, T4b, T5, P3, E3 |
| 4. Evaluate and present | Final run on 2025, once. Compare with real 2025 strategies. App tabs. README results. Talk rehearsal | E4, P4, S4, D6, L1 |

Stretch issues (X1 to X4) stay in the backlog until a pair has finished its core tasks.

Hard checkpoints for the lead: seed table in main (Phase 1), cleaning v0 done (end of Phase 2), tyre model v1 (Phase 2), cleaning v1 done (Phase 3), final 2025 run (Phase 4).

## Issues and GitHub accounts

All tasks are GitHub issues named `[ID] title`, grouped in a milestone per phase and shown on the Projects board. **Issues are created and assigned automatically from your GitHub username.** You do not create them by hand.

### How it works

1. Your username is in `scripts/issues/assignees.json`. The table above shows the same usernames. If yours is wrong or missing, tell Aziz or fix the file in a pull request.
2. You can only be assigned after you accepted the repo invitation. The script checks this and prints who has access and who does not. If you are not assigned, you do not have access yet.
3. Aziz starts the script. Two ways, both safe to run twice, because existing issues are skipped:
   - **From GitHub:** Actions, "Create project issues", Run workflow. Keep "dry run" ticked first to see what would happen, then run it again unticked.
   - **From a terminal:** `gh auth login`, then `python3 scripts/issues/create_issues.py OWNER/REPO --dry-run`, then without `--dry-run`.
4. Labels (`workstream: data`, `type: apply`, `blocked` and so on) and the phase milestones are created too.
5. In the Project, switch on the built-in workflow "Auto-add to project", so every new issue appears on the board.

### What you do with your issue

Fill in the three parts that the issue asks for: **description**, **your estimate in hours**, and **your plan or suggestions**. If the task is too big, too small or in the wrong phase, say it in a comment. The plan is a draft, and we change it together.

## How we work

- **Board columns:** Backlog, Ready, In progress, In review, Done. A task is Ready when it has owners, an estimate and a "Done when" line.
- **At most 2 items in progress per person.** A pair counts as one.
- **Review within 2 days.** Another member reviews every task.
- **Done means:** reviewed, the notebook or tests run end to end, docstrings written, docs updated if behaviour changed.
- **Pairs:** both people are assigned. Swap driver and navigator halfway. Add `Co-authored-by:` to the commit message.
- **Weekly sync, 20 minutes, Scrum style:** each person says what I did, what I do next, and what blocks me.
- **The 2025 season is a locked test set.** It is used once, in task E4. A test fails if code uses it without the explicit flag.
- **Stuck for more than a day?** Tell Aziz, and we find a pair to help.

## Workflow steps

1. **Scope:** fix circuits, seasons and constructors in `config/`.
2. **Load:** download race laps, weather and track status with FastF1 and save parquet snapshots in `data/`.
3. **Clean:** keep accurate laps only. Flag wet laps, safety car and VSC laps, red flag laps, in and out laps and lap 1. Flag outlier laps (for example slower than 107 percent of the stint median). Handle missing lap times. Map constructors to stable ids.
4. **Feature engineering:** build features per track (see below).
5. **Split:** season-based train, validation and test, with a guard so 2025 is only used with an explicit flag.
6. **Model:** baseline first, then the main model, per track.
7. **Evaluate:** validate on 2024, then run the final test on 2025 once.
8. **Present:** results table, plots and the Streamlit app.

See `docs/architecture.md` for the workflow diagram.

## Feature engineering

- **Tyre degradation:** tyre age in laps, stint number, compound, fuel-corrected lap time (lap number as a fuel burn proxy), lap time delta to the first clean lap of the stint, track and air temperature, circuit id, constructor id. Target: fuel-corrected lap time or the delta above.
- **Pit strategy:** pit loss per circuit (in lap plus out lap versus clean laps), stint lengths, number of stops, compound sequence, safety car rate per circuit from 2023 and 2024.
- **Speed profiles:** telemetry resampled on a common distance grid, speed, throttle and brake traces, minimum speed per corner, top speed, full throttle share, cumulative delta time between constructors.

## Modelling approach

- **Tyre degradation.** Baseline: linear slope per stint. Main model: gradient boosting or linear regression with circuit, compound and constructor features. STRETCH: mixed-effects model. Metric: MAE of predicted stint pace and slope error, on validation then on 2025.
- **Pit strategy.** Deterministic simulator of total race time for one-stop and two-stop strategies, using the degradation model and pit loss per circuit. STRETCH: Monte Carlo with safety car probability. Compare the recommended strategy with what teams actually ran in 2025. Metric: time delta and stop-lap agreement.
- **Speed profiles.** Descriptive: constructor comparison at 3 circuits (delta time, corner minimum speeds, top speed). STRETCH: circuit similarity.

## Tools and technologies

| Tool | Why |
|---|---|
| FastF1 | Official timing, lap and telemetry data from a free open source API |
| pandas | Tabular cleaning, filtering and joins |
| scikit-learn | Baselines and gradient boosting models |
| statsmodels | Optional mixed-effects models for degradation |
| Plotly | Interactive charts for notebooks and the app |
| Streamlit | Quick web app for the results |
| GitHub Issues, Projects and Actions | Tasks, the board, CI and the issue creation script |

## Project structure

```
f1-race-analytics/
  README.md                     # project overview, goal, scope, plan and how to run
  CONTRIBUTING.md               # how members contribute, branch and review rules
  requirements.txt              # pinned Python dependencies
  Makefile                      # common tasks (setup, lint, test, app)
  .gitignore                    # files and folders kept out of git
  config/
    settings.yaml               # shared settings for seasons, paths, thresholds and the extra rounds flag
    circuits.yaml               # the 22 circuits used in the project
    constructors.yaml           # stable constructor ids and team renames
  data/
    README.md                   # note that data files are local and gitignored
    seed/
      laps_2023_v0.parquet      # temporary seed lap table, removed when cleaning v1 matches it
      README.md                 # where the seed comes from and its limits
  notebooks/
    01_eda.ipynb                # explore coverage and lap data quality
    02_tire_degradation.ipynb   # fit and check tire degradation models
    03_pit_strategy.ipynb       # simulate and compare pit strategies
    04_speed_profiles.ipynb     # compare constructor speed profiles
  src/
    data/                       # loader.py, cleaning.py, split.py
    features/                   # tire_features.py, strategy_features.py, telemetry_features.py
    models/                     # tire_degradation.py
    strategy/                   # simulator.py
    telemetry/                  # speed_profile.py
    evaluation/                 # metrics.py, backtest.py
  models/                       # saved models, kept out of git
  app/
    app.py                      # Streamlit skeleton with sidebar filters and three tabs
  scripts/
    issues/
      issues.json               # the task list
      assignees.json            # name to GitHub username
      create_issues.py          # creates labels, milestones and issues, and assigns people
  tests/                        # test_split.py, test_cleaning.py, test_constructors.py
  docs/
    architecture.md             # workflow diagram and data flow notes
    data_contract.md            # columns of the lap table
    SCRUM.md                    # roles, cadence, definition of done and goals
    backlog.md                  # task table with owners, hours and acceptance criteria
    status.md                   # weekly update log kept by the lead
    study_notes.md              # study notes and references per member
    presentation_outline.md     # outline for the 10 minute club talk
  .github/
    workflows/ci.yml            # continuous integration with ruff and pytest
    workflows/create-issues.yml # manual workflow that creates and assigns the issues
    ISSUE_TEMPLATE/user_story.md
    pull_request_template.md
```

## How to run

```
make setup    # create .venv and install requirements
make lint     # run ruff
make test     # run pytest
make app      # start the Streamlit app
```

Run the notebooks in order: 01_eda, 02_tire_degradation, 03_pit_strategy, 04_speed_profiles. The 2025 test split only runs with an explicit flag.

## Results

Placeholder. The evaluation table and plots are filled in at the end of the project. Nothing is invented here.

## Key learnings

Placeholder. The team fills this in after the final presentation.
