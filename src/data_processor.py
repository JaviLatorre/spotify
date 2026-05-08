"""
spotify-music-intelligence · data_processor.py
Transforms raw Spotify API responses into clean, typed pandas DataFrames
ready for analysis and visualisation.

Includes the critical filter_studio_albums() function that keeps only
genuine studio albums, excluding live recordings, compilations, remasters, etc.
"""

from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

from .utils import get_logger

logger = get_logger(__name__)

# Audio feature columns returned by /audio-features endpoint
AUDIO_FEATURE_COLS = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "time_signature",
]

# Features suitable for radar/comparison charts (0-1 normalised range)
RADAR_FEATURE_COLS = [
    "danceability", "energy", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence",
]

# Keywords that indicate a non-studio release — checked against album name (lowercase)
_EXCLUDE_KEYWORDS: list[str] = [
    "live", "compilation", "reissue", "deluxe", "edition", "remix",
    "instrumental", "acoustic", "anniversary", "expanded", "remaster",
    "remastered", "best of", "greatest hits", "collection", "box set",
    "demo", "b-sides", "b sides", "rarities", "bonus", "special edition",
    "super deluxe", "tour", "concert", "unplugged", "mtv", "sessions",
    "radio", "broadcast", "bootleg", "the complete", "anthology",
]

# Regex to normalise album names for deduplication
_REMASTER_PATTERN = re.compile(
    r"\s*[\(\[]?\s*(remaster(ed)?|anniversary\s+edition|deluxe\s+edition|"
    r"super\s+deluxe|expanded\s+edition|special\s+edition|bonus\s+tracks?|"
    r"\d{4}\s+remaster|digital\s+remaster)\s*[\)\]]?\s*",
    re.IGNORECASE,
)


# ── Standalone filtering functions ────────────────────────────────────────────

def filter_studio_albums(albums_df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Filter a raw albums DataFrame to keep only genuine studio albums.

    Args:
        albums_df: DataFrame produced by DataProcessor.albums_to_df().
                   Must contain columns: album_id, name, album_type,
                   release_date, total_tracks.

    Returns:
        Tuple of (clean_df, exclusion_log) where exclusion_log is a list
        of human-readable strings explaining every rejected album.

    Filtering steps (in order):
        1. Keep only rows where album_type == "album".
        2. Exclude any album whose name contains a blacklisted keyword.
        3. Exclude EPs / mini-albums with fewer than 5 tracks.
        4. Deduplicate remasters: for albums with the same normalised name
           keep the earliest release only.
    """
    if albums_df.empty:
        return albums_df.copy(), []

    df = albums_df.copy()
    exclusion_log: list[str] = []

    # ── Step 1: album_type must be "album" ────────────────────────────────
    mask_type = df["album_type"].str.lower() == "album"
    rejected_type = df[~mask_type]["name"].tolist()
    for name in rejected_type:
        row = df[df["name"] == name].iloc[0]
        exclusion_log.append(
            f"EXCLUDED (type={row['album_type']}): {name}"
        )
    df = df[mask_type].copy()
    logger.info("After type filter: %d albums kept, %d excluded", len(df), len(rejected_type))

    # ── Step 2: Keyword exclusion ─────────────────────────────────────────
    def _has_excluded_keyword(album_name: str) -> bool:
        lower = album_name.lower()
        return any(kw in lower for kw in _EXCLUDE_KEYWORDS)

    mask_kw = ~df["name"].apply(_has_excluded_keyword)
    rejected_kw = df[~mask_kw]["name"].tolist()
    for name in rejected_kw:
        matched = next(kw for kw in _EXCLUDE_KEYWORDS if kw in name.lower())
        exclusion_log.append(f"EXCLUDED (keyword='{matched}'): {name}")
    df = df[mask_kw].copy()
    logger.info("After keyword filter: %d albums kept, %d excluded", len(df), len(rejected_kw))

    # ── Step 3: Exclude EPs / mini-albums (< 5 tracks) ───────────────────
    mask_tracks = df["total_tracks"].fillna(0) >= 5
    rejected_ep = df[~mask_tracks]["name"].tolist()
    for name in rejected_ep:
        tracks = df[df["name"] == name]["total_tracks"].iloc[0]
        exclusion_log.append(f"EXCLUDED (EP, tracks={tracks}): {name}")
    df = df[mask_tracks].copy()
    logger.info("After EP filter: %d albums kept, %d excluded", len(df), len(rejected_ep))

    # ── Step 4: Deduplicate remasters (keep earliest per normalised name) ─
    def _normalise_name(name: str) -> str:
        """Strip remaster/edition suffixes to get a canonical title."""
        cleaned = _REMASTER_PATTERN.sub("", name)
        return cleaned.strip().lower()

    df["_norm_name"] = df["name"].apply(_normalise_name)
    df_sorted = df.sort_values("release_date", na_position="last")

    # Keep first occurrence per normalised name (oldest release = original)
    before_dedup = len(df_sorted)
    df_dedup = df_sorted.drop_duplicates(subset="_norm_name", keep="first")
    rejected_dedup = df_sorted[~df_sorted.index.isin(df_dedup.index)]["name"].tolist()
    for name in rejected_dedup:
        exclusion_log.append(f"EXCLUDED (duplicate/remaster): {name}")

    df_final = df_dedup.drop(columns=["_norm_name"]).reset_index(drop=True)
    logger.info(
        "After deduplication: %d albums kept, %d excluded",
        len(df_final), before_dedup - len(df_final),
    )

    logger.info(
        "filter_studio_albums() final: %d studio albums from %d raw albums",
        len(df_final), len(albums_df),
    )
    return df_final, exclusion_log


def aggregate_features(tracks_df: pd.DataFrame) -> dict[str, Any]:
    """Compute summary statistics for all numeric audio features.

    Args:
        tracks_df: Merged tracks + audio features DataFrame.

    Returns:
        Dict mapping feature name → {"mean", "std", "min", "max", "median"}.
    """
    numeric_cols = [c for c in AUDIO_FEATURE_COLS if c in tracks_df.columns]
    result: dict[str, Any] = {}
    for col in numeric_cols:
        series = tracks_df[col].dropna()
        if series.empty:
            continue
        result[col] = {
            "mean": round(float(series.mean()), 4),
            "std": round(float(series.std()), 4),
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
            "median": round(float(series.median()), 4),
        }
    return result


def feature_evolution(tracks_df: pd.DataFrame) -> dict[str, Any]:
    """Compute per-year average of each audio feature.

    Args:
        tracks_df: Merged DataFrame that includes a 'release_date' column.

    Returns:
        Dict with:
            "years": sorted list of years
            "<feature>": list of mean values aligned with years
    """
    df = tracks_df.copy()
    if "release_date" not in df.columns:
        logger.warning("feature_evolution: 'release_date' column missing")
        return {}

    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    numeric_cols = [c for c in RADAR_FEATURE_COLS if c in df.columns]
    grouped = df.groupby("year")[numeric_cols].mean().round(4)

    result: dict[str, Any] = {"years": grouped.index.tolist()}
    for col in numeric_cols:
        result[col] = grouped[col].tolist()
    return result


def compare_artists_features(
    artist1_df: pd.DataFrame,
    artist2_df: pd.DataFrame,
    artist1_name: str = "Artist 1",
    artist2_name: str = "Artist 2",
) -> dict[str, Any]:
    """Compare audio feature distributions between two artists.

    Args:
        artist1_df: Merged tracks DataFrame for artist 1.
        artist2_df: Merged tracks DataFrame for artist 2.
        artist1_name: Display name for artist 1.
        artist2_name: Display name for artist 2.

    Returns:
        Dict with per-feature stats for each artist plus absolute difference.
    """
    cols = [c for c in RADAR_FEATURE_COLS if c in artist1_df.columns and c in artist2_df.columns]
    result: dict[str, Any] = {
        "features": cols,
        artist1_name: {},
        artist2_name: {},
        "difference": {},
    }
    for col in cols:
        m1 = float(artist1_df[col].mean())
        m2 = float(artist2_df[col].mean())
        result[artist1_name][col] = round(m1, 4)
        result[artist2_name][col] = round(m2, 4)
        result["difference"][col] = round(abs(m1 - m2), 4)
    return result


# ── DataProcessor class ───────────────────────────────────────────────────────

class DataProcessor:
    """Converts Spotify API dicts to analysis-ready DataFrames."""

    # ── Tracks ────────────────────────────────────────────────────────────

    @staticmethod
    def tracks_to_df(tracks: list[dict[str, Any]]) -> pd.DataFrame:
        """Convert raw track dicts from Spotify API to a DataFrame.

        Args:
            tracks: List of track objects returned by the Spotify API.

        Returns:
            DataFrame with one row per track.
        """
        rows = []
        for t in tracks:
            artists = ", ".join(a["name"] for a in t.get("artists", []))
            rows.append(
                {
                    "track_id": t["id"],
                    "name": t["name"],
                    "artists": artists,
                    "album": t.get("album", {}).get("name", ""),
                    "release_date": t.get("album", {}).get("release_date", ""),
                    "duration_ms": t.get("duration_ms"),
                    "popularity": t.get("popularity"),
                    "explicit": t.get("explicit", False),
                    "preview_url": t.get("preview_url"),
                }
            )
        df = pd.DataFrame(rows)
        if not df.empty:
            df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
            df["duration_min"] = (df["duration_ms"] / 60_000).round(2)
        return df

    # ── Audio features ────────────────────────────────────────────────────

    @staticmethod
    def audio_features_to_df(features: list[dict[str, Any]]) -> pd.DataFrame:
        """Convert raw audio-feature dicts to a DataFrame.

        Args:
            features: List of audio feature objects from Spotify API.

        Returns:
            DataFrame with one row per track.
        """
        rows = []
        for f in features:
            row = {"track_id": f.get("id")}
            row.update({col: f.get(col) for col in AUDIO_FEATURE_COLS})
            rows.append(row)
        return pd.DataFrame(rows)

    # ── Albums ────────────────────────────────────────────────────────────

    @staticmethod
    def albums_to_df(albums: list[dict[str, Any]]) -> pd.DataFrame:
        """Convert raw album dicts to a DataFrame.

        Args:
            albums: List of album objects from Spotify API.

        Returns:
            DataFrame with one row per album.
        """
        rows = []
        for a in albums:
            rows.append(
                {
                    "album_id": a["id"],
                    "name": a["name"],
                    "album_type": a.get("album_type"),
                    "release_date": a.get("release_date"),
                    "total_tracks": a.get("total_tracks"),
                    "label": a.get("label", ""),
                    "popularity": a.get("popularity"),
                    "image_url": (a.get("images") or [{}])[0].get("url"),
                }
            )
        df = pd.DataFrame(rows)
        if not df.empty:
            df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        return df

    # ── Merge helpers ─────────────────────────────────────────────────────

    @staticmethod
    def merge_tracks_features(
        tracks_df: pd.DataFrame,
        features_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Left-join track metadata with audio features on track_id.

        Args:
            tracks_df: Output of tracks_to_df().
            features_df: Output of audio_features_to_df().

        Returns:
            Merged DataFrame.
        """
        return tracks_df.merge(features_df, on="track_id", how="left", suffixes=("", "_feat"))

    # ── Normalisation ─────────────────────────────────────────────────────

    @staticmethod
    def normalise_features(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
        """Min-max normalise selected columns (returns a copy).

        Args:
            df: DataFrame to normalise.
            cols: Columns to normalise; defaults to AUDIO_FEATURE_COLS present in df.

        Returns:
            New DataFrame with specified columns normalised to [0, 1].
        """
        cols = cols or [c for c in AUDIO_FEATURE_COLS if c in df.columns]
        out = df.copy()
        for col in cols:
            col_min, col_max = out[col].min(), out[col].max()
            if col_max > col_min:
                out[col] = (out[col] - col_min) / (col_max - col_min)
        return out

    # ── Convenience wrappers around module-level functions ────────────────

    @staticmethod
    def filter_studio_albums(
        albums_df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, list[str]]:
        """Alias for the module-level filter_studio_albums() function."""
        return filter_studio_albums(albums_df)

    @staticmethod
    def aggregate_features(tracks_df: pd.DataFrame) -> dict[str, Any]:
        """Alias for the module-level aggregate_features() function."""
        return aggregate_features(tracks_df)

    @staticmethod
    def feature_evolution(tracks_df: pd.DataFrame) -> dict[str, Any]:
        """Alias for the module-level feature_evolution() function."""
        return feature_evolution(tracks_df)

    @staticmethod
    def compare_artists_features(
        artist1_df: pd.DataFrame,
        artist2_df: pd.DataFrame,
        artist1_name: str = "Artist 1",
        artist2_name: str = "Artist 2",
    ) -> dict[str, Any]:
        """Alias for the module-level compare_artists_features() function."""
        return compare_artists_features(artist1_df, artist2_df, artist1_name, artist2_name)
