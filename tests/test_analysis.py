"""
spotify-music-intelligence · tests/test_analysis.py
Unit tests for DataProcessor and NLPAnalyzer.
"""

from __future__ import annotations

import pandas as pd
import pytest

from src.data_processor import DataProcessor
from src.nlp_analyzer import NLPAnalyzer


# ── DataProcessor ──────────────────────────────────────────────────────────

SAMPLE_TRACKS = [
    {
        "id": "t1",
        "name": "Track One",
        "artists": [{"name": "Artist A"}],
        "album": {"name": "Album X", "release_date": "2020-01-01"},
        "duration_ms": 210000,
        "popularity": 75,
        "explicit": False,
        "preview_url": None,
    }
]

SAMPLE_FEATURES = [
    {
        "id": "t1",
        "danceability": 0.8,
        "energy": 0.6,
        "key": 5,
        "loudness": -6.0,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.7,
        "tempo": 120.0,
        "duration_ms": 210000,
        "time_signature": 4,
    }
]


def test_tracks_to_df_shape():
    df = DataProcessor.tracks_to_df(SAMPLE_TRACKS)
    assert len(df) == 1
    assert "duration_min" in df.columns


def test_audio_features_to_df_columns():
    df = DataProcessor.audio_features_to_df(SAMPLE_FEATURES)
    assert "danceability" in df.columns
    assert df["danceability"].iloc[0] == pytest.approx(0.8)


def test_merge_tracks_features():
    t_df = DataProcessor.tracks_to_df(SAMPLE_TRACKS)
    f_df = DataProcessor.audio_features_to_df(SAMPLE_FEATURES)
    merged = DataProcessor.merge_tracks_features(t_df, f_df)
    assert "energy" in merged.columns


def test_normalise_features_range():
    t_df = DataProcessor.tracks_to_df(SAMPLE_TRACKS * 3)
    f_df = DataProcessor.audio_features_to_df(
        [{**SAMPLE_FEATURES[0], "id": f"t{i}", "energy": i * 0.3} for i in range(3)]
    )
    f_df["track_id"] = [f"t{i}" for i in range(3)]
    normed = DataProcessor.normalise_features(f_df, cols=["energy"])
    assert normed["energy"].min() >= 0.0
    assert normed["energy"].max() <= 1.0


# ── NLPAnalyzer ───────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def analyzer():
    return NLPAnalyzer()


SAMPLE_LYRICS = (
    "We carry on, through the storm and the rain\n"
    "We find our way back home again\n"
    "The world is dark but love remains"
)


def test_sentiment_keys(analyzer):
    result = analyzer.sentiment(SAMPLE_LYRICS)
    assert "polarity" in result
    assert "subjectivity" in result
    assert result["label"] in {"positive", "negative", "neutral"}


def test_top_keywords_count(analyzer):
    kw = analyzer.top_keywords(SAMPLE_LYRICS, n=5)
    assert len(kw) <= 5
    assert all(isinstance(w, str) and isinstance(c, int) for w, c in kw)


def test_readability_metrics(analyzer):
    metrics = analyzer.readability_metrics(SAMPLE_LYRICS)
    assert metrics["word_count"] > 0
    assert 0.0 <= metrics["lexical_diversity"] <= 1.0


def test_analyse_corpus_returns_df(analyzer):
    corpus = [
        {"track_id": "t1", "title": "Song A", "lyrics": SAMPLE_LYRICS},
        {"track_id": "t2", "title": "Song B", "lyrics": "I feel so alone, lost in the dark"},
    ]
    df = analyzer.analyse_corpus(corpus)
    assert len(df) == 2
    assert "polarity" in df.columns
