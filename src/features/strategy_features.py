"""builds pit strategy features per circuit.

Steps to implement:
1. Compute pit loss per circuit from the in lap and out lap delta.
2. Compute stint lengths and the number of stops.
3. Build the compound sequence per driver and race.
4. Compute the safety car rate per circuit from 2023 and 2024 only.
5. Estimate an undercut window per circuit.
6. Return one frame ready for the strategy simulator.
"""

from __future__ import annotations

import pandas as pd


def compute_pit_loss(laps: pd.DataFrame) -> pd.DataFrame:
    """Compute the pit loss per circuit from in lap and out lap deltas."""
    raise NotImplementedError


def compute_stint_lengths(laps: pd.DataFrame) -> pd.DataFrame:
    """Compute the stint length for every stint."""
    raise NotImplementedError


def compute_stop_counts(laps: pd.DataFrame) -> pd.DataFrame:
    """Compute the number of stops per driver and race."""
    raise NotImplementedError


def compute_safety_car_rate(laps: pd.DataFrame) -> pd.DataFrame:
    """Compute the safety car rate per circuit from 2023 and 2024."""
    raise NotImplementedError


def build_strategy_features(laps: pd.DataFrame) -> pd.DataFrame:
    """Combine all pit strategy features into one frame."""
    raise NotImplementedError
