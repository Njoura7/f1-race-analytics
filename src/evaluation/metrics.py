"""metric helpers for pace and strategy evaluation.

Steps to implement:
1. Mean absolute error for stint pace.
2. Slope error between true and predicted degradation slopes.
3. Stop lap agreement between actual and recommended strategies.
"""

from __future__ import annotations

import pandas as pd


def mae(y_true: pd.Series, y_pred: pd.Series) -> float:
    """Return the mean absolute error between two series."""
    raise NotImplementedError


def slope_error(true_slope: float, pred_slope: float) -> float:
    """Return the absolute difference between two degradation slopes."""
    raise NotImplementedError


def stop_lap_agreement(actual: list[int], predicted: list[int]) -> float:
    """Return the share of predicted stop laps that match the actual ones."""
    raise NotImplementedError
