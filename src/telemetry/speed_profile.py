"""compares constructor speed profiles per circuit.

Steps to implement:
1. Build the speed trace per constructor on the shared distance grid.
2. Combine traces into one profile frame per circuit.
3. Compute the cumulative delta time between constructors.
4. Return the comparison table used by the notebook and the app.
"""

from __future__ import annotations

import pandas as pd


def speed_trace_by_constructor(telemetry: pd.DataFrame) -> pd.DataFrame:
    """Return the speed trace per constructor on the shared distance grid."""
    raise NotImplementedError


def cumulative_delta(telemetry: pd.DataFrame) -> pd.DataFrame:
    """Return the cumulative delta time between constructors."""
    raise NotImplementedError


def compare_constructors(profiles: pd.DataFrame) -> pd.DataFrame:
    """Return a comparison table of constructor speed profiles."""
    raise NotImplementedError
