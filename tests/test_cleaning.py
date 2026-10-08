"""placeholder tests for the lap filters.

TODO: replace the skipped test once cleaning.py is implemented.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO: implement cleaning.py and test the lap filters")
def test_outlier_laps_are_flagged() -> None:
    """Check that slow laps are flagged as outliers."""
