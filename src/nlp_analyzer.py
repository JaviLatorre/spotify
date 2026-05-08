"""
spotify-music-intelligence · nlp_analyzer.py
NLP pipeline for lyric analysis: VADER sentiment, TF-IDF keywords,
n-gram extraction, Word2Vec embeddings, and readability metrics.

Dependencies: nltk, vaderSentiment, scikit-learn, gensim (optional).
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from .utils import get_logger

logger = get_logger(__name__)

# ── NLTK resource bootstrap ───────────────────────────────────────────────────

_NLTK_RESOURCES = [
    ("tokenizers/punkt", "punkt"),
    ("tokenizers/punkt_tab", "punkt_tab"),
    ("corpora/stopwords", "stopwords"),
    ("corpora/wordnet", "wordnet"),
    ("sentiment/vader_lexicon", "vader_lexicon"),
]


def _ensure_nltk() -> None:
    """Download required NLTK data packages if not already present."""
    for path, pkg in _NLTK_RESOURCES:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)


# ── Metadata patterns to strip from lyrics ───────────────────────────────────

_METADATA_PATTERN = re.compile(
    r"\[(?:Verse|Chorus|Bridge|Intro|Outro|Hook|Pre-Chorus|Interlude|Refrain|"
    r"Spoken|Instrumental|Coda|Break|Skit|Solo|Vamp|Tag|Adlib|Fade|Repeat)"
    r"[^\]]*\]",
    re.IGNORECASE,
)


# ── Main analyser class ───────────────────────────────────────────────────────

class LyricsAnalyzer:
    """Full NLP pipeline for song lyric analysis.

    Provides sentiment scoring (VADER), TF-IDF keywords, n-gram analysis,
    lexical diversity, Word2Vec embeddings, and per-artist aggregation.
    """

    def __init__(self, language: str = "english") -> None:
        _ensure_nltk()

        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer

        self._stopwords: set[str] = set(stopwords.words(language))
        self._stopwords.update(
            {"verse", "chorus", "bridge", "outro", "intro", "hook",
             "yeah", "oh", "ah", "uh", "la", "hey", "ooh", "na"}
        )
        self._lemmatizer = WordNetLemmatizer()

        # VADER sentiment analyser
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self._vader = SentimentIntensityAnalyzer()
            logger.debug("Using vaderSentiment package")
        except ImportError:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer  # type: ignore
            self._vader = SentimentIntensityAnalyzer()
            logger.debug("Using nltk VADER")

    # ── Text preprocessing ────────────────────────────────────────────────

    def clean_text(self, text: str) -> str:
        """Remove structural metadata and normalise whitespace.

        Args:
            text: Raw lyrics string.

        Returns:
            Cleaned lyrics string suitable for NLP analysis.
        """
        text = _METADATA_PATTERN.sub("", text)        # remove [Verse 1] etc.
        text = re.sub(r"\(.*?\)", "", text)            # remove parenthetical stage directions
        text = re.sub(r"[^\w\s'']", " ", text)        # keep words, spaces, apostrophes
        text = re.sub(r"[ \t]+", " ", text)            # collapse horizontal whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)         # max 2 consecutive newlines
        return text.strip()

    def tokenize(self, text: str) -> list[str]:
        """Tokenize and lemmatize a lyrics string.

        Args:
            text: Cleaned lyrics text.

        Returns:
            List of lowercase lemmatized tokens with stopwords removed.
        """
        from nltk.tokenize import word_tokenize

        cleaned = self.clean_text(text)
        tokens = word_tokenize(cleaned.lower())
        return [
            self._lemmatizer.lemmatize(tok)
            for tok in tokens
            if tok.isalpha() and tok not in self._stopwords and len(tok) > 2
        ]

    # ── Feature extraction ────────────────────────────────────────────────

    def extract_features(self, lyrics_text: str) -> dict[str, Any]:
        """Extract a comprehensive NLP feature set from a lyrics string.

        Args:
            lyrics_text: Raw or lightly cleaned lyrics.

        Returns:
            Dict containing:
                word_freq (dict): top-50 word frequencies
                unique_words (int): count of distinct words
                avg_word_length (float): mean word length
                diversity_ratio (float): unique/total word ratio
                sentiment_score (float): VADER compound score in [-1, 1]
                sentiment_label (str): positive / neutral / negative
                vader_detail (dict): pos, neg, neu, compound breakdown
                top_ngrams (list): top-10 bigrams as (phrase, count) pairs
                tfidf_keywords (list): TF-IDF top keywords (if corpus available)
        """
        cleaned = self.clean_text(lyrics_text)
        tokens = self.tokenize(lyrics_text)

        # Word frequency
        freq = Counter(tokens)
        top50 = dict(freq.most_common(50))

        # Lexical stats
        total_words = len(tokens)
        unique_words = len(freq)
        avg_word_length = (
            float(np.mean([len(w) for w in tokens])) if tokens else 0.0
        )
        diversity_ratio = round(unique_words / max(total_words, 1), 4)

        # VADER sentiment
        scores = self._vader.polarity_scores(cleaned)
        compound = scores["compound"]
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"

        # N-grams (bigrams)
        try:
            bigram_vec = CountVectorizer(ngram_range=(2, 2), max_features=20)
            bigram_vec.fit([cleaned])
            bigram_counts = bigram_vec.transform([cleaned]).toarray()[0]
            vocab = bigram_vec.get_feature_names_out()
            top_bigrams = sorted(
                zip(vocab, bigram_counts.tolist()),
                key=lambda x: x[1], reverse=True
            )[:10]
            top_ngrams = [(str(phrase), int(cnt)) for phrase, cnt in top_bigrams if cnt > 0]
        except Exception:
            top_ngrams = []

        return {
            "word_freq": top50,
            "unique_words": unique_words,
            "total_words": total_words,
            "avg_word_length": round(avg_word_length, 2),
            "diversity_ratio": diversity_ratio,
            "sentiment_score": round(compound, 4),
            "sentiment_label": label,
            "vader_detail": {
                "positive": round(scores["pos"], 4),
                "negative": round(scores["neg"], 4),
                "neutral": round(scores["neu"], 4),
                "compound": round(scores["compound"], 4),
            },
            "top_ngrams": top_ngrams,
        }

    # ── Artist-level aggregation ──────────────────────────────────────────

    def analyze_artist_lyrics(self, lyrics_list: list[str]) -> dict[str, Any]:
        """Aggregate NLP features across all a single artist's lyrics.

        Args:
            lyrics_list: List of raw lyrics strings for one artist.

        Returns:
            Dict with mean sentiment, pooled word frequency, TF-IDF keywords,
            and per-song sentiment list.
        """
        if not lyrics_list:
            return {}

        sentiments = []
        all_tokens: list[str] = []
        per_song_sentiments = []

        for lyrics in lyrics_list:
            feats = self.extract_features(lyrics)
            sentiments.append(feats["sentiment_score"])
            all_tokens.extend(self.tokenize(lyrics))
            per_song_sentiments.append(feats["sentiment_score"])

        pooled_freq = Counter(all_tokens)
        top50_pooled = dict(pooled_freq.most_common(50))

        # TF-IDF across all songs
        tfidf_keywords = self._tfidf_keywords(lyrics_list, top_n=20)

        return {
            "song_count": len(lyrics_list),
            "mean_sentiment": round(float(np.mean(sentiments)), 4),
            "std_sentiment": round(float(np.std(sentiments)), 4),
            "positive_pct": round(sum(s > 0.05 for s in sentiments) / len(sentiments), 4),
            "negative_pct": round(sum(s < -0.05 for s in sentiments) / len(sentiments), 4),
            "neutral_pct": round(sum(-0.05 <= s <= 0.05 for s in sentiments) / len(sentiments), 4),
            "word_freq": top50_pooled,
            "tfidf_keywords": tfidf_keywords,
            "per_song_sentiments": per_song_sentiments,
            "total_words": len(all_tokens),
            "unique_words": len(pooled_freq),
            "lexical_diversity": round(len(pooled_freq) / max(len(all_tokens), 1), 4),
        }

    def compare_artists(
        self,
        artist1_lyrics: list[str],
        artist2_lyrics: list[str],
        artist1_name: str = "Artist 1",
        artist2_name: str = "Artist 2",
    ) -> dict[str, Any]:
        """Compare NLP profiles of two artists.

        Args:
            artist1_lyrics: List of raw lyrics for artist 1.
            artist2_lyrics: List of raw lyrics for artist 2.
            artist1_name: Display name for artist 1.
            artist2_name: Display name for artist 2.

        Returns:
            Side-by-side comparison dict with difference metrics.
        """
        a1 = self.analyze_artist_lyrics(artist1_lyrics)
        a2 = self.analyze_artist_lyrics(artist2_lyrics)

        metrics = [
            "mean_sentiment", "std_sentiment",
            "positive_pct", "negative_pct", "lexical_diversity",
        ]
        comparison: dict[str, Any] = {
            artist1_name: a1,
            artist2_name: a2,
            "difference": {},
        }
        for m in metrics:
            v1 = a1.get(m, 0.0)
            v2 = a2.get(m, 0.0)
            comparison["difference"][m] = round(abs(v1 - v2), 4)  # type: ignore[assignment]

        return comparison

    # ── Word2Vec embeddings ───────────────────────────────────────────────

    def get_embeddings(
        self,
        text: str,
        vector_size: int = 50,
        window: int = 5,
        min_count: int = 1,
    ) -> np.ndarray | None:
        """Train a small Word2Vec model on the given text and return centroid.

        Args:
            text: Lyrics or large text corpus.
            vector_size: Dimensionality of word vectors.
            window: Context window size.
            min_count: Minimum word frequency to include.

        Returns:
            Mean embedding vector of shape (vector_size,), or None if gensim
            is unavailable or the corpus is too small.
        """
        try:
            from gensim.models import Word2Vec  # type: ignore
        except ImportError:
            logger.warning("gensim not installed — Word2Vec embeddings unavailable")
            return None

        tokens = self.tokenize(text)
        if len(tokens) < 5:
            logger.warning("get_embeddings: corpus too small (%d tokens)", len(tokens))
            return None

        # Word2Vec requires list-of-sentences
        sentences = [tokens]
        model = Word2Vec(
            sentences,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            workers=1,
            epochs=10,
        )
        vectors = np.array([model.wv[w] for w in tokens if w in model.wv])
        if len(vectors) == 0:
            return None
        return np.mean(vectors, axis=0)

    def get_embeddings_corpus(
        self,
        lyrics_list: list[str],
        vector_size: int = 100,
    ) -> tuple[np.ndarray | None, list[str]]:
        """Train Word2Vec on a full corpus and return per-song centroids.

        Args:
            lyrics_list: List of raw lyrics strings.
            vector_size: Embedding dimensionality.

        Returns:
            Tuple of (embeddings_matrix, vocabulary) where embeddings_matrix has
            shape (n_songs, vector_size), or (None, []) if gensim unavailable.
        """
        try:
            from gensim.models import Word2Vec  # type: ignore
        except ImportError:
            logger.warning("gensim not installed — corpus embeddings unavailable")
            return None, []

        all_sentences = [self.tokenize(lyrics) for lyrics in lyrics_list]
        all_sentences = [s for s in all_sentences if s]
        if not all_sentences:
            return None, []

        model = Word2Vec(
            all_sentences,
            vector_size=vector_size,
            window=5,
            min_count=2,
            workers=1,
            epochs=15,
        )

        embeddings = []
        for tokens in all_sentences:
            vecs = [model.wv[w] for w in tokens if w in model.wv]
            if vecs:
                embeddings.append(np.mean(vecs, axis=0))
            else:
                embeddings.append(np.zeros(vector_size))

        return np.array(embeddings), list(model.wv.key_to_index.keys())

    # ── TF-IDF ────────────────────────────────────────────────────────────

    def _tfidf_keywords(self, documents: list[str], top_n: int = 20) -> list[tuple[str, float]]:
        """Extract top TF-IDF keywords across a collection of documents.

        Args:
            documents: List of text documents.
            top_n: Number of keywords to return.

        Returns:
            List of (keyword, tfidf_score) tuples sorted by score descending.
        """
        if len(documents) < 2:
            return []
        try:
            stop_list = list(self._stopwords)
            vec = TfidfVectorizer(
                max_features=500,
                stop_words=stop_list,
                ngram_range=(1, 2),
                min_df=1,
            )
            matrix = vec.fit_transform(documents)
            mean_scores = np.asarray(matrix.mean(axis=0)).flatten()
            feature_names = vec.get_feature_names_out()
            indices = mean_scores.argsort()[::-1][:top_n]
            return [
                (str(feature_names[i]), round(float(mean_scores[i]), 6))
                for i in indices
            ]
        except Exception as exc:
            logger.error("TF-IDF failed: %s", exc)
            return []

    def tfidf_keywords(self, documents: list[str], top_n: int = 20) -> list[tuple[str, float]]:
        """Public wrapper for TF-IDF keyword extraction.

        Args:
            documents: List of lyrics strings (one per song or per artist).
            top_n: Number of top keywords to return.

        Returns:
            List of (keyword, tfidf_score) sorted descending.
        """
        return self._tfidf_keywords(documents, top_n=top_n)

    # ── Corpus analysis ───────────────────────────────────────────────────

    def analyse_corpus(self, tracks: list[dict[str, str]]) -> pd.DataFrame:
        """Analyse a list of track dicts and return a feature DataFrame.

        Args:
            tracks: List of dicts with keys track_id, title, lyrics.

        Returns:
            DataFrame with one row per track containing all NLP features.
        """
        rows = []
        for t in tracks:
            lyrics = t.get("lyrics", "")
            if not lyrics:
                continue
            feats = self.extract_features(lyrics)
            row: dict[str, Any] = {
                "track_id": t.get("track_id", ""),
                "title": t.get("title", ""),
            }
            row["polarity"] = feats["sentiment_score"]
            row["compound"] = feats["vader_detail"]["compound"]
            row["positive"] = feats["vader_detail"]["positive"]
            row["negative"] = feats["vader_detail"]["negative"]
            row["neutral"] = feats["vader_detail"]["neutral"]
            row["subjectivity"] = 0.0  # VADER does not compute subjectivity
            row["label"] = feats["sentiment_label"]
            row["word_count"] = feats["total_words"]
            row["unique_words"] = feats["unique_words"]
            row["avg_word_length"] = feats["avg_word_length"]
            row["lexical_diversity"] = feats["diversity_ratio"]
            row["top_keywords"] = ", ".join(
                list(feats["word_freq"].keys())[:5]
            )
            rows.append(row)
        return pd.DataFrame(rows)

    # ── Backward-compatible sentiment method ──────────────────────────────

    def sentiment(self, text: str) -> dict[str, float]:
        """Return VADER sentiment scores for a text.

        Args:
            text: Input text.

        Returns:
            Dict with polarity (compound), subjectivity (0.0), and label.
        """
        scores = self._vader.polarity_scores(text)
        compound = scores["compound"]
        return {
            "polarity": round(compound, 4),
            "subjectivity": 0.0,
            "label": (
                "positive" if compound >= 0.05
                else "negative" if compound <= -0.05
                else "neutral"
            ),
        }

    def top_keywords(self, text: str, n: int = 20) -> list[tuple[str, int]]:
        """Return the top-n most frequent non-stopword tokens.

        Args:
            text: Input text.
            n: Number of keywords to return.

        Returns:
            List of (word, count) tuples.
        """
        tokens = self.tokenize(text)
        return Counter(tokens).most_common(n)

    def readability_metrics(self, text: str) -> dict[str, Any]:
        """Compute basic readability / lexical richness metrics.

        Args:
            text: Input text.

        Returns:
            Dict with word_count, unique_words, sentence_count,
            avg_sentence_length, and lexical_diversity.
        """
        cleaned = self.clean_text(text)
        sentences = [s.strip() for s in re.split(r"[.!?\n]", cleaned) if s.strip()]
        words = cleaned.split()
        unique = set(w.lower() for w in words)
        return {
            "word_count": len(words),
            "unique_words": len(unique),
            "sentence_count": len(sentences),
            "avg_sentence_length": round(len(words) / max(len(sentences), 1), 2),
            "lexical_diversity": round(len(unique) / max(len(words), 1), 4),
        }


# ── Module-level alias (matches prompt spec) ─────────────────────────────────

NLPAnalyzer = LyricsAnalyzer
