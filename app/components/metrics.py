"""
spotify-music-intelligence · app/components/metrics.py
Styled metric display components for Streamlit dashboards.
"""

from __future__ import annotations

import streamlit as st


def show_metric(
    label: str,
    value: str | int | float,
    icon: str = "",
    delta: str | None = None,
) -> None:
    """Display a single styled metric card.

    Args:
        label: Metric name / description.
        value: The value to display (string, int, or float).
        icon: Optional emoji prefix.
        delta: Optional delta string shown below the value (green/red).
    """
    display_value = f"{value:,}" if isinstance(value, int) else str(value)
    label_text = f"{icon} {label}".strip()
    st.metric(label=label_text, value=display_value, delta=delta)


def show_metrics_row(metrics: list[dict]) -> None:
    """Display a horizontal row of metric cards.

    Args:
        metrics: List of dicts, each with keys:
                 - label (str): Metric name
                 - value (str|int|float): The value
                 - icon (str, optional): Emoji prefix
                 - delta (str, optional): Delta value
    """
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            show_metric(
                label=metric.get("label", ""),
                value=metric.get("value", "—"),
                icon=metric.get("icon", ""),
                delta=metric.get("delta"),
            )
