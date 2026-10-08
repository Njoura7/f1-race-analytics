"""Streamlit skeleton with sidebar filters and three tabs.

Steps to implement:
1. Replace the placeholder lists with circuits and constructors from config/.
2. Load the saved results and show them in each tab.
3. Keep the filter selections in the sidebar.
4. Add plots once the notebooks produce results.
"""

from __future__ import annotations

import streamlit as st


def sidebar_filters() -> tuple[str, str]:
    """Render the circuit and constructor filters and return the selections."""
    circuits = ["Placeholder circuit"]
    constructors = ["Placeholder constructor"]
    circuit = st.sidebar.selectbox("Circuit", circuits)
    constructor = st.sidebar.selectbox("Constructor", constructors)
    return circuit, constructor


def main() -> None:
    """Render the app skeleton with three tabs and placeholder text."""
    st.title("F1 Telemetry and Race Analytics")
    circuit, constructor = sidebar_filters()
    st.caption(f"Selected circuit: {circuit}")
    st.caption(f"Selected constructor: {constructor}")

    tab_degradation, tab_strategy, tab_speed = st.tabs(
        ["Tire degradation", "Pit strategy", "Speed profiles"]
    )
    with tab_degradation:
        st.write("Placeholder for tire degradation results.")
    with tab_strategy:
        st.write("Placeholder for pit strategy results.")
    with tab_speed:
        st.write("Placeholder for speed profile results.")


if __name__ == "__main__":
    main()
