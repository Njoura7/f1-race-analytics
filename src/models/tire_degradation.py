"""fits the tire degradation baseline and main model.

Steps to implement:
1. Fit a simple linear slope per stint as the baseline.
2. Fit the main model per track with gradient boosting or linear regression,
   using circuit, compound and constructor features.
3. Predict stint pace and per-constructor slopes.
4. Save artifacts under models/.
5. STRETCH: replace the main model with a mixed-effects model.
"""

from __future__ import annotations

import pandas as pd


def fit_linear_baseline(features: pd.DataFrame) -> dict[str, float]:
    """Fit the linear slope baseline and return its coefficients."""
    raise NotImplementedError


def fit_main_model(features: pd.DataFrame) -> object:
    """Fit the main degradation model per track and return it."""
    raise NotImplementedError


def predict_pace(model: object, features: pd.DataFrame) -> pd.Series:
    """Predict stint pace for the given features."""
    raise NotImplementedError
