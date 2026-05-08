"""
spotify-music-intelligence · app/components/sidebar.py
Reusable sidebar input widgets shared across app pages.
"""

from __future__ import annotations

import streamlit as st

_AUDIO_FEATURES = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo",
]

_DEFAULT_ARTISTS = ["Radiohead", "Pink Floyd", "The Beatles", "Nirvana", "David Bowie"]


def artist_selector(
    label: str = "Select artist",
    options: list[str] | None = None,
    key: str = "artist_selector",
) -> str:
    """Render a sidebar selectbox for artist selection.

    Args:
        label: Widget label text.
        options: List of artist names to display. Falls back to common defaults.
        key: Streamlit widget key.

    Returns:
        Selected artist name string.
    """
    choices = options or _DEFAULT_ARTISTS
    return st.sidebar.selectbox(label, choices, key=key)


def feature_selector(
    label: str = "Select audio features",
    default: list[str] | None = None,
    key: str = "feature_selector",
) -> list[str]:
    """Render a sidebar multiselect for audio feature selection.

    Args:
        label: Widget label text.
        default: Pre-selected features; defaults to first 5 radar features.
        key: Streamlit widget key.

    Returns:
        List of selected feature name strings.
    """
    defaults = default or _AUDIO_FEATURES[:5]
    return st.sidebar.multiselect(
        label,
        options=_AUDIO_FEATURES,
        default=defaults,
        key=key,
    )


def date_range_slider(
    min_year: int = 1960,
    max_year: int = 2024,
    key: str = "year_range",
) -> tuple[int, int]:
    """Render a sidebar slider for selecting a release year range.

    Args:
        min_year: Minimum selectable year.
        max_year: Maximum selectable year.
        key: Streamlit widget key.

    Returns:
        Tuple of (start_year, end_year).
    """
    return st.sidebar.slider(
        "Release year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key=key,
    )
