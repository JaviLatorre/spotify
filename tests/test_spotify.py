"""
spotify-music-intelligence · tests/test_spotify.py
Unit tests for SpotifyClient using mocked Spotipy responses.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.spotify_api import SpotifyClient


@pytest.fixture()
def mock_client():
    with patch("src.spotify_api.SpotifyClientCredentials"), \
         patch("src.spotify_api.spotipy.Spotify") as mock_sp:
        mock_sp.return_value = MagicMock()
        yield SpotifyClient()


def test_search_artist_returns_list(mock_client):
    mock_client._client.search.return_value = {
        "artists": {"items": [{"id": "abc", "name": "Radiohead"}]}
    }
    results = mock_client.search_artist("Radiohead")
    assert isinstance(results, list)
    assert results[0]["name"] == "Radiohead"


def test_get_audio_features_batches(mock_client):
    mock_client._client.audio_features.return_value = [
        {"id": f"t{i}", "danceability": 0.5} for i in range(10)
    ]
    ids = [f"t{i}" for i in range(10)]
    features = mock_client.get_audio_features(ids)
    assert len(features) == 10


def test_get_artist_albums_paginates(mock_client):
    mock_client._client.artist_albums.return_value = {
        "items": [{"id": "a1", "name": "Album 1"}],
        "next": None,
    }
    albums = mock_client.get_artist_albums("artist_id")
    assert len(albums) == 1


def test_get_recommendations(mock_client):
    mock_client._client.recommendations.return_value = {
        "tracks": [{"id": "t1", "name": "Track"}]
    }
    result = mock_client.get_recommendations(seed_genres=["rock"])
    assert len(result) == 1
