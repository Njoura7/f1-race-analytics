"""runs validation on 2024 and the final test on 2025.

Steps to implement:
1. Score the model on the 2024 validation season.
2. Refuse to touch 2025 unless allow_test is true.
3. Run the single final test on 2025.
4. Assemble the evaluation table with validation and test rows.
"""

from __future__ import annotations

import pandas as pd


def run_validation(model: object, data: pd.DataFrame) -> pd.DataFrame:
    """Score the model on the 2024 validation season."""
    raise NotImplementedError


def run_final_test(model: object, data: pd.DataFrame, allow_test: bool = False) -> pd.DataFrame:
    """Run the single final test on 2025 and require an explicit flag."""
    raise NotImplementedError


def evaluation_table(validation: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    """Combine validation and test scores into one table."""
    raise NotImplementedError
