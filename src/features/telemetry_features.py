"""builds speed profile features on a distance grid.

Steps to implement:
1. Resample car telemetry on a common distance grid for each fastest lap.
2. Extract speed, throttle and brake traces.
3. Segment the corners from the circuit info.
4. Compute the minimum speed per corner, the top speed and the full throttle share.
5. Compute the cumulative delta time between constructors.
6. Return one frame with the telemetry features per constructor and circuit.
"""

from __future__ import annotations

import pandas as pd


def resample_telemetry(telemetry: pd.DataFrame, grid_step: float = 25.0) -> pd.DataFrame:
    """Resample telemetry on a common distance grid."""
    raise NotImplementedError


def segment_corners(circuit_info: object) -> pd.DataFrame:
    """Segment the corners of a circuit from the circuit info."""
    raise NotImplementedError


def compute_corner_min_speed(telemetry: pd.DataFrame, corners: pd.DataFrame) -> pd.DataFrame:
    """Compute the minimum speed per corner."""
    raise NotImplementedError


def build_telemetry_features(telemetry: pd.DataFrame, circuit_info: object) -> pd.DataFrame:
    """Combine all speed profile features into one frame."""
    raise NotImplementedError
