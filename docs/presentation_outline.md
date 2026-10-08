# Presentation outline

A 10 minute talk for the club. Six sections, one or two bullets each.

## 1. Goal and scope

- One goal: constructor-level models of tire degradation and pit strategy, plus a speed profile comparison.
- Three questions: tyre pace loss, best pit strategy versus what teams did, and speed profile differences.

## 2. Data and split

- FastF1 race data from 22 circuits, with a local cache and light cleaning.
- Train on 2023, validate on 2024, test once on 2025.

## 3. Repo structure

- Clear folders: config, data, notebooks, src, app, tests and docs.
- One notebook and one module group per analysis track.

## 4. Tools

- FastF1 and pandas for data, scikit-learn and statsmodels for models.
- Plotly for charts and Streamlit for the demo app.

## 5. Model approach per track

- Tire degradation: linear baseline, then mixed-effects or gradient boosting per track.
- Pit strategy: Monte Carlo from the degradation model and pit loss. Speed profiles: descriptive comparisons and delta time.

## 6. Plan and roles

- Five sprints, weekly sync, one review and retro per sprint.
- Roles: A data, B degradation, C strategy, D speed, E evaluation and app, lead runs the process.
