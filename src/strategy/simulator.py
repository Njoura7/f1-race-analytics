"""simulates race time for one-stop and two-stop pit strategies.

Steps to implement:
1. Simulate total race time from the degradation model and pit loss per circuit.
2. Score one-stop and two-stop candidates and pick the smallest total time.
3. Compare the recommended strategy with the strategies run in 2025.
4. STRETCH: add Monte Carlo safety car events with a per-circuit probability.
"""

from __future__ import annotations


def simulate_strategy(
    strategy: list[int],
    degradation: object,
    pit_loss: float,
) -> dict[str, float]:
    """Simulate one pit strategy and return its total race time."""
    raise NotImplementedError


def recommend_strategy(
    candidates: list[list[int]],
    degradation: object,
    pit_loss: float,
) -> list[int]:
    """Return the candidate strategy with the smallest total race time."""
    raise NotImplementedError


def compare_to_actual(recommended: list[int], actual: list[int]) -> dict[str, float]:
    """Compare the recommended strategy with the actual strategy."""
    raise NotImplementedError
