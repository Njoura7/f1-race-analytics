"""simulates race time for candidate pit strategies.

Steps to implement:
1. Simulate total race time from the degradation model and pit loss per circuit.
2. Draw safety car events from the per-circuit probability with Monte Carlo.
3. Score every candidate strategy and pick the smallest total time.
4. Compare the recommended strategy with the strategies run in 2025.
"""

from __future__ import annotations


def simulate_strategy(
    strategy: list[int],
    degradation: object,
    pit_loss: float,
    sc_probability: float,
    n_runs: int = 1000,
) -> dict[str, float]:
    """Simulate one pit strategy and return a summary of total race times."""
    raise NotImplementedError


def recommend_strategy(candidates: list[list[int]], **kwargs: float) -> list[int]:
    """Return the candidate strategy with the smallest total race time."""
    raise NotImplementedError


def compare_to_actual(recommended: list[int], actual: list[int]) -> dict[str, float]:
    """Compare the recommended strategy with the actual strategy."""
    raise NotImplementedError
