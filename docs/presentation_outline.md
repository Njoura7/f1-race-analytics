# Presentation outline

A 10 minute talk for the club. Six sections, one or two bullets each.

## 1. Goal and scope

- One goal: constructor-level models of tire degradation and pit strategy, plus a speed profile comparison.
- Official race sessions only, 22 shared circuits, 3 seasons.

## 2. Data and split

- FastF1 race laps, weather and track status, with a local cache and light cleaning.
- Train on 2023, validate on 2024, test once on 2025.

## 3. Repo structure

- Clear folders: config, data, notebooks, src, app, tests and docs.
- One notebook and one module group per analysis track.

## 4. Tools

- FastF1 and pandas for data, scikit-learn and statsmodels for models.
- Plotly for charts and Streamlit for the demo app.

## 5. Model approach per track

- Tire degradation: linear baseline, then gradient boosting or linear regression. Pit strategy: deterministic one-stop and two-stop simulator.
- Speed profiles: descriptive comparison at 3 circuits. STRETCH marked in the README.

## 6. Plan and roles

- Three one-week sprints: study and data, build, evaluate and present.
- Roles: A data, B degradation, C strategy, D speed, E evaluation and app, lead runs the process.
