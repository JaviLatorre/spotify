"""
spotify-music-intelligence · visualization.py
Reusable Plotly and Altair chart builders for audio features, lyrics NLP,
sentiment timelines, and artist comparison dashboards.

All Plotly functions return go.Figure objects.
All Altair functions return alt.Chart / alt.LayerChart objects.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .utils import get_logger

logger = get_logger(__name__)

_RADAR_FEATURES = [
    "danceability", "energy", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence",
]

_COLOR_PALETTE = px.colors.qualitative.Set2
_VIRIDIS = px.colors.sequential.Viridis


# ═══════════════════════════════════════════════════════════════════════════════
# PLOTLY — interactive charts
# ═══════════════════════════════════════════════════════════════════════════════

def plot_word_cloud(word_freq_dict: dict[str, int | float], max_words: int = 80) -> go.Figure:
    """Render a Plotly-based word cloud (scatter with text sized by frequency).

    Args:
        word_freq_dict: Mapping of word → frequency count.
        max_words: Maximum number of words to display.

    Returns:
        Plotly Figure with a scatter-text word cloud using Viridis colour scale.
    """
    import random
    import math

    if not word_freq_dict:
        return go.Figure().update_layout(title="No word data available")

    items = sorted(word_freq_dict.items(), key=lambda x: x[1], reverse=True)[:max_words]
    words, counts = zip(*items)
    max_count = max(counts)

    # Arrange words in a pseudo-random scatter
    random.seed(42)
    n = len(words)
    angles = [i * (2 * math.pi / n) for i in range(n)]
    radii = [random.uniform(0.2, 1.0) for _ in range(n)]
    x_vals = [r * math.cos(a) for r, a in zip(radii, angles)]
    y_vals = [r * math.sin(a) for r, a in zip(radii, angles)]
    sizes = [8 + 42 * (c / max_count) for c in counts]
    colours = [c / max_count for c in counts]

    fig = go.Figure(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="text",
            text=list(words),
            textfont={
                "size": sizes,
                "color": [f"rgb({int(255*v)},{int(180*(1-v))},{int(200*(1-v))})" for v in colours],
            },
            hovertemplate=[f"<b>{w}</b><br>Count: {c}<extra></extra>" for w, c in zip(words, counts)],
        )
    )
    fig.update_layout(
        title="Word Cloud",
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="#1a1a2e",
        font_color="white",
    )
    return fig


def plot_top_words_bar(
    word_freq: dict[str, int | float],
    top_n: int = 20,
    title: str = "Top Words by Frequency",
) -> go.Figure:
    """Horizontal bar chart of the most frequent words.

    Args:
        word_freq: Word → frequency mapping.
        top_n: Number of words to display.
        title: Chart title.

    Returns:
        Plotly Figure sorted by frequency (highest on top).
    """
    items = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    if not items:
        return go.Figure().update_layout(title="No word data")

    words = [w for w, _ in items]
    counts = [c for _, c in items]

    fig = go.Figure(
        go.Bar(
            x=counts[::-1],
            y=words[::-1],
            orientation="h",
            marker_color=px.colors.sequential.Plasma_r[:len(words)],
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Frequency",
        yaxis_title="Word",
        height=max(300, 22 * top_n),
        margin={"l": 120},
    )
    return fig


def plot_sentiment_timeline(
    lyrics_by_year: dict[int, list[float]],
    artist_name: str = "Artist",
) -> go.Figure:
    """Line chart of VADER compound sentiment aggregated by release year.

    Args:
        lyrics_by_year: Mapping of year → list of compound sentiment scores.
        artist_name: Used in the chart title.

    Returns:
        Plotly Figure with a rangeslider for zooming.
    """
    if not lyrics_by_year:
        return go.Figure().update_layout(title="No sentiment data")

    years = sorted(lyrics_by_year.keys())
    means = [float(pd.Series(lyrics_by_year[y]).mean()) for y in years]
    pos_pct = [sum(s > 0.05 for s in lyrics_by_year[y]) / max(len(lyrics_by_year[y]), 1) for y in years]
    neg_pct = [sum(s < -0.05 for s in lyrics_by_year[y]) / max(len(lyrics_by_year[y]), 1) for y in years]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=means, mode="lines+markers", name="Mean Sentiment",
        line={"color": "#1DB954", "width": 2},
        hovertemplate="Year: %{x}<br>Mean: %{y:.3f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=pos_pct, mode="lines", name="% Positive",
        line={"color": "#2ecc71", "dash": "dot"},
    ))
    fig.add_trace(go.Scatter(
        x=years, y=neg_pct, mode="lines", name="% Negative",
        line={"color": "#e74c3c", "dash": "dot"},
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")

    fig.update_layout(
        title=f"Sentiment Timeline — {artist_name}",
        xaxis_title="Year",
        yaxis_title="Sentiment Score",
        xaxis={"rangeslider": {"visible": True}},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02},
        height=450,
    )
    return fig


def plot_feature_scatter(
    tracks_df: pd.DataFrame,
    x_feature: str,
    y_feature: str,
    color_by: str = "album",
) -> go.Figure:
    """Interactive scatter plot of two audio features.

    Args:
        tracks_df: Merged tracks DataFrame with audio features.
        x_feature: Column name for the X axis.
        y_feature: Column name for the Y axis.
        color_by: Column to use for colour coding (e.g. album, release_year).

    Returns:
        Plotly scatter Figure with hover info and size by duration.
    """
    df = tracks_df.copy()
    size_col = None
    if "duration_ms" in df.columns:
        df["_size"] = (df["duration_ms"] / 1000).clip(upper=600)
        size_col = "_size"

    fig = px.scatter(
        df,
        x=x_feature,
        y=y_feature,
        color=color_by if color_by in df.columns else None,
        size=size_col,
        hover_name="name" if "name" in df.columns else None,
        hover_data={c: True for c in ["album", "release_date", "popularity"] if c in df.columns},
        title=f"{x_feature.title()} vs {y_feature.title()}",
        opacity=0.75,
        color_continuous_scale="Viridis",
    )
    if size_col:
        fig.update_traces(selector={"type": "scatter"})
        df.drop(columns=["_size"], inplace=True, errors="ignore")
    return fig


def plot_feature_evolution(
    artist_tracks_df: pd.DataFrame,
    artist_name: str = "Artist",
    features: list[str] | None = None,
) -> go.Figure:
    """Line chart showing how audio features changed over time.

    Args:
        artist_tracks_df: Merged DataFrame with release_date column.
        artist_name: Used in the chart title.
        features: List of feature column names to plot; defaults to radar features.

    Returns:
        Plotly Figure with one line per feature and a rangeslider.
    """
    df = artist_tracks_df.copy()
    if "release_date" not in df.columns:
        return go.Figure().update_layout(title="Missing release_date column")

    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    plot_features = features or [f for f in _RADAR_FEATURES if f in df.columns]
    yearly = df.groupby("year")[plot_features].mean().reset_index()

    fig = go.Figure()
    colours = px.colors.qualitative.Plotly
    for i, feat in enumerate(plot_features):
        fig.add_trace(go.Scatter(
            x=yearly["year"],
            y=yearly[feat],
            mode="lines+markers",
            name=feat.title(),
            line={"color": colours[i % len(colours)], "width": 2},
            hovertemplate=f"{feat}: %{{y:.3f}}<br>Year: %{{x}}<extra></extra>",
        ))

    fig.update_layout(
        title=f"Feature Evolution Over Time — {artist_name}",
        xaxis_title="Year",
        yaxis_title="Mean Feature Value",
        xaxis={"rangeslider": {"visible": True}},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02},
        height=450,
    )
    return fig


def plot_artist_comparison_radar(artists_data_dict: dict[str, dict[str, float]]) -> go.Figure:
    """Radar chart comparing up to 3 artists across audio and NLP features.

    Args:
        artists_data_dict: Mapping of artist_name → {feature: value, ...}.
                           All values should be in [0, 1].

    Returns:
        Plotly radar Figure.
    """
    if not artists_data_dict:
        return go.Figure().update_layout(title="No artist data")

    artists = list(artists_data_dict.keys())[:3]
    all_features = sorted(
        {f for a in artists for f in artists_data_dict[a].keys()}
    )
    if not all_features:
        return go.Figure().update_layout(title="No features available")

    colours = ["#1DB954", "#1E90FF", "#FF6B6B"]
    fig = go.Figure()
    for i, artist in enumerate(artists):
        vals = [artists_data_dict[artist].get(f, 0.0) for f in all_features]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=all_features + [all_features[0]],
            fill="toself",
            name=artist,
            line_color=colours[i % len(colours)],
            opacity=0.7,
        ))

    fig.update_layout(
        polar={"radialaxis": {"visible": True, "range": [0, 1]}},
        showlegend=True,
        title="Artist Feature Comparison (Radar)",
        height=500,
    )
    return fig


def plot_heatmap_features_year(
    tracks_df: pd.DataFrame,
    features: list[str] | None = None,
) -> go.Figure:
    """Heatmap of mean feature value per release year.

    Args:
        tracks_df: Merged DataFrame with release_date and audio feature columns.
        features: Feature columns to include; defaults to _RADAR_FEATURES.

    Returns:
        Plotly heatmap Figure (years on X axis, features on Y axis).
    """
    df = tracks_df.copy()
    if "release_date" not in df.columns:
        return go.Figure().update_layout(title="Missing release_date")

    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    plot_features = features or [f for f in _RADAR_FEATURES if f in df.columns]
    if not plot_features:
        return go.Figure().update_layout(title="No feature columns found")

    pivot = df.groupby("year")[plot_features].mean().T.round(3)

    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=[f.title() for f in pivot.index.tolist()],
            colorscale="Viridis",
            hovertemplate="Feature: %{y}<br>Year: %{x}<br>Value: %{z:.3f}<extra></extra>",
            text=pivot.values.round(2),
            texttemplate="%{text}",
        )
    )
    fig.update_layout(
        title="Audio Features Heatmap (Year × Feature)",
        xaxis_title="Year",
        yaxis_title="Feature",
        height=400,
    )
    return fig


# ── Backward-compatible Visualizer class ─────────────────────────────────────

class Visualizer:
    """Factory wrapper exposing chart functions as static methods."""

    @staticmethod
    def radar_chart(df: pd.DataFrame, track_col: str = "name") -> go.Figure:
        """Radar chart comparing audio features across tracks."""
        features = [f for f in _RADAR_FEATURES if f in df.columns]
        fig = go.Figure()
        for i, (_, row) in enumerate(df.iterrows()):
            vals = [row[f] for f in features]
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=features + [features[0]],
                fill="toself",
                name=str(row.get(track_col, f"Track {i}")),
                line_color=_COLOR_PALETTE[i % len(_COLOR_PALETTE)],
            ))
        fig.update_layout(
            polar={"radialaxis": {"visible": True, "range": [0, 1]}},
            showlegend=True,
            title="Audio Features Radar",
        )
        return fig

    @staticmethod
    def feature_distribution(df: pd.DataFrame, feature: str) -> go.Figure:
        fig = px.histogram(df, x=feature, nbins=30, title=f"Distribution: {feature}")
        fig.update_layout(bargap=0.1)
        return fig

    @staticmethod
    def feature_scatter(
        df: pd.DataFrame,
        x: str,
        y: str,
        color: str | None = None,
        hover: str | None = None,
    ) -> go.Figure:
        return px.scatter(
            df, x=x, y=y, color=color, hover_name=hover,
            title=f"{x.title()} vs {y.title()}",
            opacity=0.75,
        )

    @staticmethod
    def discography_timeline(albums_df: pd.DataFrame) -> go.Figure:
        df = albums_df.sort_values("release_date").copy()
        fig = px.scatter(
            df,
            x="release_date",
            y="popularity",
            size="total_tracks",
            hover_name="name",
            color="album_type",
            title="Discography Timeline",
        )
        return fig

    @staticmethod
    def sentiment_bar(nlp_df: pd.DataFrame) -> go.Figure:
        df = nlp_df.sort_values("polarity")
        fig = px.bar(
            df, x="title", y="polarity",
            color="label",
            color_discrete_map={
                "positive": "#2ecc71",
                "neutral": "#95a5a6",
                "negative": "#e74c3c",
            },
            title="Lyric Sentiment by Track",
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig

    @staticmethod
    def sentiment_scatter(nlp_df: pd.DataFrame) -> go.Figure:
        return px.scatter(
            nlp_df, x="polarity", y="subjectivity",
            hover_name="title", color="label",
            title="Sentiment Space",
            labels={"polarity": "Compound Score", "subjectivity": "Subjectivity"},
        )

    @staticmethod
    def correlation_heatmap(df: pd.DataFrame, cols: list[str]) -> go.Figure:
        corr = df[cols].corr().round(2)
        fig = go.Figure(go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr.values,
            texttemplate="%{text}",
        ))
        fig.update_layout(title="Feature Correlation Heatmap")
        return fig

    # ── Convenience wrappers for new standalone functions ─────────────────

    @staticmethod
    def word_cloud(word_freq_dict: dict[str, int | float]) -> go.Figure:
        return plot_word_cloud(word_freq_dict)

    @staticmethod
    def top_words_bar(word_freq: dict[str, int | float], top_n: int = 20) -> go.Figure:
        return plot_top_words_bar(word_freq, top_n=top_n)

    @staticmethod
    def sentiment_timeline(lyrics_by_year: dict[int, list[float]], artist_name: str = "") -> go.Figure:
        return plot_sentiment_timeline(lyrics_by_year, artist_name)

    @staticmethod
    def feature_evolution(tracks_df: pd.DataFrame, artist_name: str = "") -> go.Figure:
        return plot_feature_evolution(tracks_df, artist_name)

    @staticmethod
    def comparison_radar(artists_data_dict: dict[str, dict[str, float]]) -> go.Figure:
        return plot_artist_comparison_radar(artists_data_dict)

    @staticmethod
    def features_heatmap(tracks_df: pd.DataFrame) -> go.Figure:
        return plot_heatmap_features_year(tracks_df)


# ═══════════════════════════════════════════════════════════════════════════════
# ALTAIR — dynamic dashboards
# ═══════════════════════════════════════════════════════════════════════════════

def _altair_available() -> bool:
    try:
        import altair  # noqa: F401
        return True
    except ImportError:
        return False


def create_album_dashboard(albums_df: pd.DataFrame):  # type: ignore[return]
    """Altair interactive album catalogue with artist selector and sortable columns.

    Args:
        albums_df: DataProcessor.albums_to_df() output, optionally pre-filtered.

    Returns:
        alt.Chart or None if altair is not installed.
    """
    if not _altair_available():
        logger.warning("altair not installed — returning None")
        return None

    import altair as alt  # type: ignore

    df = albums_df.copy()
    if "release_date" in df.columns:
        df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year.fillna(0).astype(int)

    cols = [c for c in ["name", "year", "total_tracks", "album_type", "popularity"] if c in df.columns]
    df_display = df[cols].rename(columns={
        "name": "Album",
        "year": "Year",
        "total_tracks": "Tracks",
        "album_type": "Type",
        "popularity": "Popularity",
    })

    brush = alt.selection_single(name="album_sel", fields=["Type"], bind="legend")

    bars = (
        alt.Chart(df_display)
        .mark_bar()
        .encode(
            x=alt.X("Tracks:Q", title="Number of Tracks"),
            y=alt.Y("Album:N", sort="-x", title=None),
            color=alt.Color("Type:N", scale=alt.Scale(scheme="set2")),
            opacity=alt.condition(brush, alt.value(1), alt.value(0.3)),
            tooltip=["Album:N", "Year:Q", "Tracks:Q", "Type:N", "Popularity:Q"],
        )
        .add_selection(brush)
        .properties(title="Studio Albums", height=max(200, 28 * len(df_display)), width=600)
    )
    return bars


def create_lyrics_dashboard(
    artist_lyrics_dict: dict[str, dict[str, int]],
    artist_name: str = "Artist",
):  # type: ignore[return]
    """Altair word-frequency bar chart with interactive highlight.

    Args:
        artist_lyrics_dict: Mapping of word → frequency count.
        artist_name: Display title.

    Returns:
        alt.Chart or None if altair is not installed.
    """
    if not _altair_available():
        return None

    import altair as alt  # type: ignore

    items = sorted(artist_lyrics_dict.items(), key=lambda x: x[1], reverse=True)[:25]
    df = pd.DataFrame(items, columns=["word", "count"])

    selector = alt.selection_single(on="mouseover", fields=["word"], empty="none")

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="Frequency"),
            y=alt.Y("word:N", sort="-x", title=None),
            color=alt.condition(
                selector,
                alt.value("#1DB954"),
                alt.value("#cccccc"),
            ),
            tooltip=["word:N", "count:Q"],
        )
        .add_selection(selector)
        .properties(title=f"Top Words — {artist_name}", height=600, width=500)
    )
    return chart


def create_comparison_dashboard(artists_data: dict[str, dict[str, float]]):  # type: ignore[return]
    """Altair side-by-side feature comparison for up to 3 artists.

    Args:
        artists_data: Mapping of artist_name → {feature: value, ...}.

    Returns:
        alt.Chart or None if altair is not installed.
    """
    if not _altair_available():
        return None

    import altair as alt  # type: ignore

    rows = []
    for artist, features in list(artists_data.items())[:3]:
        for feature, value in features.items():
            rows.append({"artist": artist, "feature": feature.title(), "value": round(value, 4)})

    df = pd.DataFrame(rows)
    if df.empty:
        return None

    artist_sel = alt.selection_multi(fields=["artist"], bind="legend")

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("feature:N", title=None),
            y=alt.Y("value:Q", title="Mean Value", scale=alt.Scale(domain=[0, 1])),
            color=alt.Color("artist:N", scale=alt.Scale(scheme="tableau10")),
            xOffset="artist:N",
            opacity=alt.condition(artist_sel, alt.value(0.9), alt.value(0.2)),
            tooltip=["artist:N", "feature:N", "value:Q"],
        )
        .add_selection(artist_sel)
        .properties(title="Artist Feature Comparison", width=700, height=350)
    )
    return chart
