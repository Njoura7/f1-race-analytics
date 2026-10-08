"""builds tire degradation features per stint.

Steps to implement:
1. Add tyre age in laps from the stint start.
2. Add fuel-corrected lap time using the lap number as a fuel burn proxy.
3. Add the lap time delta to the first clean lap of the stint.
4. Keep stint number, compound, track and air temperature, circuit id and constructor id.
5. Return one frame ready for the degradation model.
"""

from __future__ import annotations

import pandas as pd


def add_tyre_age(laps: pd.DataFrame) -> pd.DataFrame:
    """Add the tyre age in laps for each stint."""
    raise NotImplementedError


def add_fuel_corrected_lap_time(laps: pd.DataFrame) -> pd.DataFrame:
    """Add a fuel-corrected lap time using the lap number as a fuel burn proxy."""
    raise NotImplementedError


def add_stint_delta(laps: pd.DataFrame) -> pd.DataFrame:
    """Add the lap time delta to the first clean lap of the stint."""
    raise NotImplementedError


def build_tire_features(laps: pd.DataFrame) -> pd.DataFrame:
    """Combine all tire degradation features into one frame."""
    raise NotImplementedError
