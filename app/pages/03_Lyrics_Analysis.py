"""
Página 3 — Análisis de Letras
Obtiene letras de lyrics.ovh y analiza:
- nº de palabras
- palabras más frecuentes
- diversidad léxica

REQUISITO 2 (4 puntos):
Componente de exploración de letras.
"""

from __future__ import annotations

import json
import re
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Análisis de Letras",
    page_icon="📝",
    layout="wide"
)

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

CACHE_DIR = DATA_DIR / "lyrics_cache"
CACHE_DIR.mkdir(exist_ok=True)

ARTIST = "Radiohead"

# ──────────────────────────────────────────────────────────────────────────────
# STOPWORDS
# ──────────────────────────────────────────────────────────────────────────────

_STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "you", "your", "he", "she", "it",
    "they", "them", "what", "which", "who", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "shall", "can", "a", "an", "the", "and", "but", "if", "or",
    "as", "at", "by", "for", "in", "of", "on", "to", "up", "with", "so",
    "yet", "both", "not", "no", "nor", "too", "very", "just", "there",
    "their", "his", "her", "its", "then", "than", "when", "where", "how",
    "all", "any", "each", "more", "most", "other", "some", "such", "only",
    "own", "same", "never", "now", "oh", "yeah", "don't", "don", "t",
    "won't", "won", "ain't", "ain", "ll", "ve", "re", "s", "d", "m",
    "get", "got", "let", "like", "know", "go", "going", "come", "back",
    "want", "need", "say", "said", "see", "make", "made", "one", "two",
    "into", "about", "out", "from", "every", "again", "here", "even",
    "cause", "because", "well", "still", "over", "down",
}

# ──────────────────────────────────────────────────────────────────────────────
# DATA LOADERS
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_tracks() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_tracks.json"
    return pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))


@st.cache_data
def load_albums() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_albums.json"
    return pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

def clean_title(title: str) -> str:
    """
    Limpia títulos problemáticos:
    - (Remastered)
    - - 2011 Remaster
    - Live
    """
    title = re.sub(r"\(.*?\)", "", title)
    title = re.sub(r"- .*", "", title)
    return title.strip()


def safe_filename(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)


def clean_and_tokenize(text: str) -> list[str]:
    """
    Limpia texto y tokeniza.
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)

    tokens = [
        w for w in text.split()
        if w not in _STOPWORDS and len(w) > 1
    ]

    return tokens

# ──────────────────────────────────────────────────────────────────────────────
# FETCH LYRICS
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def fetch_lyrics(artist: str, title: str) -> str | None:
    """
    Obtiene letras desde lyrics.ovh.
    Usa caché local para evitar peticiones repetidas.
    """

    try:
        artist_clean = artist.strip()
        title_clean = clean_title(title)

        # ── CACHE LOCAL ───────────────────────────────────────────────────────

        cache_file = CACHE_DIR / f"{safe_filename(title_clean)}.txt"

        if cache_file.exists():
            cached = cache_file.read_text(encoding="utf-8").strip()

            if cached:
                return cached

        # ── API REQUEST ──────────────────────────────────────────────────────

        url = f"https://api.lyrics.ovh/v1/{artist_clean}/{title_clean}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=8
        )

        if r.status_code == 200:
            data = r.json()

            lyrics = data.get("lyrics", "").strip()

            if lyrics and "Instrumental" not in lyrics:

                # guardar caché
                cache_file.write_text(
                    lyrics,
                    encoding="utf-8"
                )

                return lyrics

        return None

    except Exception:
        return None

# ──────────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────────

st.title("📝 Análisis de Letras")
st.caption(
    "Exploración de letras usando lyrics.ovh"
)

tracks_df = load_tracks()
albums_df = load_albums()

if tracks_df.empty:
    st.error(
        "No se encontraron datos. "
        "Ejecuta generate_data.py primero."
    )
    st.stop()

album_order = (
    albums_df
    .sort_values("year")["name"]
    .tolist()
)

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────

with st.sidebar:

    st.header("⚙️ Filtros")

    selected_albums = st.multiselect(
        "Álbumes",
        album_order,
        default=album_order
    )

    top_n = st.slider(
        "Top palabras",
        min_value=10,
        max_value=40,
        value=20
    )

    st.info(
        "Las letras se obtienen desde lyrics.ovh.\n\n"
        "Algunas canciones pueden no estar disponibles."
    )

# ──────────────────────────────────────────────────────────────────────────────
# FILTER DATA
# ──────────────────────────────────────────────────────────────────────────────

df = tracks_df[
    tracks_df["album"].isin(selected_albums)
].copy()

if df.empty:
    st.warning("No hay canciones disponibles.")
    st.stop()

# ──────────────────────────────────────────────────────────────────────────────
# FETCH LYRICS
# ──────────────────────────────────────────────────────────────────────────────

st.subheader("Obteniendo letras...")

track_lyrics: dict[str, str] = {}

progress = st.progress(0)

total = len(df)

for idx, (_, row) in enumerate(df.iterrows()):

    song_name = row["name"]

    progress.progress(
        (idx + 1) / total,
        text=f"Buscando: {song_name}"
    )

    lyrics = fetch_lyrics(
        ARTIST,
        song_name
    )

    if lyrics:
        track_lyrics[song_name] = lyrics

    time.sleep(0.05)

progress.empty()

found = len(track_lyrics)
missing = total - found

c1, c2 = st.columns(2)

c1.success(
    f"✅ Letras encontradas: {found}/{total}"
)

if missing > 0:
    c2.warning(
        f"⚠️ Canciones sin letras disponibles: {missing}"
    )

if not track_lyrics:
    st.error(
        "No se pudieron obtener letras desde lyrics.ovh."
    )
    st.stop()

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# ANALYTICS
# ──────────────────────────────────────────────────────────────────────────────

word_counts = []
all_tokens = []

for _, row in df.iterrows():

    song = row["name"]
    album = row["album"]

    lyrics = track_lyrics.get(song)

    if not lyrics:
        continue

    tokens = clean_and_tokenize(lyrics)

    raw_words = len(lyrics.split())
    unique_words = len(set(tokens))

    all_tokens.extend(tokens)

    lexical_diversity = (
        unique_words / max(len(tokens), 1)
    )

    word_counts.append({
        "Canción": song,
        "Álbum": album,
        "Palabras totales": raw_words,
        "Palabras únicas": unique_words,
        "Diversidad léxica": round(
            lexical_diversity,
            3
        )
    })

wc_df = pd.DataFrame(word_counts)

# ──────────────────────────────────────────────────────────────────────────────
# METRICS
# ──────────────────────────────────────────────────────────────────────────────

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "🎵 Canciones",
    found
)

m2.metric(
    "📝 Palabras totales",
    f"{wc_df['Palabras totales'].sum():,}"
)

m3.metric(
    "📚 Media palabras/canción",
    f"{wc_df['Palabras totales'].mean():.0f}"
)

m4.metric(
    "🔤 Palabras únicas",
    len(set(all_tokens))
)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# CHART 1
# ──────────────────────────────────────────────────────────────────────────────

st.subheader("Número de palabras por canción")

wc_sorted = wc_df.sort_values(
    "Palabras totales",
    ascending=True
)

fig_wc = px.bar(
    wc_sorted,
    x="Palabras totales",
    y="Canción",
    color="Álbum",
    orientation="h",
    height=max(400, len(wc_df) * 22),
)

st.plotly_chart(
    fig_wc,
    use_container_width=True
)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# CHART 2
# ──────────────────────────────────────────────────────────────────────────────

st.subheader(
    f"Top {top_n} palabras más frecuentes"
)

freq = Counter(all_tokens).most_common(top_n)

freq_df = pd.DataFrame(
    freq,
    columns=["Palabra", "Frecuencia"]
)

fig_freq = px.bar(
    freq_df,
    x="Frecuencia",
    y="Palabra",
    orientation="h",
    color="Frecuencia",
    color_continuous_scale="Greens",
    height=max(400, top_n * 22),
)

fig_freq.update_layout(
    yaxis={"categoryorder": "total ascending"},
    coloraxis_showscale=False
)

st.plotly_chart(
    fig_freq,
    use_container_width=True
)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# DETAIL VIEW
# ──────────────────────────────────────────────────────────────────────────────

st.subheader("Detalle por canción")

available_tracks = list(track_lyrics.keys())

selected_track = st.selectbox(
    "Selecciona una canción",
    available_tracks
)

lyrics_text = track_lyrics[selected_track]

tokens = clean_and_tokenize(lyrics_text)

top15 = Counter(tokens).most_common(15)

ca, cb, cc = st.columns(3)

ca.metric(
    "Palabras totales",
    len(lyrics_text.split())
)

cb.metric(
    "Palabras únicas",
    len(set(tokens))
)

cc.metric(
    "Diversidad léxica",
    f"{len(set(tokens))/max(len(tokens),1):.3f}"
)

col1, col2 = st.columns([1, 1])

with col1:

    st.markdown("### Letra")

    st.text_area(
        "",
        lyrics_text,
        height=350,
        label_visibility="collapsed"
    )

with col2:

    st.markdown("### Top 15 palabras")

    top15_df = pd.DataFrame(
        top15,
        columns=["Palabra", "Frecuencia"]
    )

    fig_top15 = px.bar(
        top15_df,
        x="Frecuencia",
        y="Palabra",
        orientation="h",
        color="Frecuencia",
        color_continuous_scale="Oranges",
        height=350
    )

    fig_top15.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_top15,
        use_container_width=True
    )

# ──────────────────────────────────────────────────────────────────────────────
# FULL TABLE
# ──────────────────────────────────────────────────────────────────────────────

with st.expander("📊 Tabla completa"):

    st.dataframe(
        wc_df.sort_values(
            "Palabras totales",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )