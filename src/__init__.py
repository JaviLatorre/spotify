"""
spotify-music-intelligence · src package
Exposes the primary modules for external imports.
"""

from .config import Settings
from .spotify_api import SpotifyClient
from .lyrics_handler import LyricsHandler
from .data_processor import DataProcessor
from .nlp_analyzer import NLPAnalyzer
from .visualization import Visualizer
from .utils import get_logger

__all__ = [
    "Settings",
    "SpotifyClient",
    "LyricsHandler",
    "DataProcessor",
    "NLPAnalyzer",
    "Visualizer",
    "get_logger",
]
