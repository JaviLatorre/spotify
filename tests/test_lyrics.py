"""
spotify-music-intelligence · tests/test_lyrics.py
Unit tests for LyricsHandler: cache behaviour, cleaning, and provider fallback.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.lyrics_handler import LyricsHandler


@pytest.fixture()
def handler(tmp_path, monkeypatch):
    cfg = MagicMock()
    cfg.cache_dir = tmp_path
    cfg.genius_api_token = ""
    cfg.musixmatch_api_key = ""
    cfg.request_timeout = 10
    return LyricsHandler(settings=cfg)


def test_clean_removes_tags():
    cleaned = LyricsHandler._clean("[Verse 1]\nHello world\n\n\n\nBye")
    assert "[Verse 1]" not in cleaned
    assert "Hello world" in cleaned


def test_cache_key_is_deterministic():
    k1 = LyricsHandler._cache_key("Artist", "Title")
    k2 = LyricsHandler._cache_key("artist", "title")
    assert k1 == k2


def test_disk_cache_roundtrip(handler, tmp_path):
    key = LyricsHandler._cache_key("Test", "Song")
    lyrics = "La la la"
    handler._save_to_disk(key, lyrics)
    result = handler._load_from_disk(key)
    assert result == lyrics


def test_get_lyrics_no_providers_returns_none(handler):
    result = handler.get_lyrics("Unknown Artist", "Unknown Song")
    assert result is None


def test_get_lyrics_uses_memory_cache(handler):
    key = LyricsHandler._cache_key("A", "B")
    handler._mem_cache[key] = "Cached lyrics"
    result = handler.get_lyrics("A", "B")
    assert result == "Cached lyrics"
