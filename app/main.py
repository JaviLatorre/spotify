"""
spotify-music-intelligence · app/main.py
Punto de entrada de la web app Streamlit.
Funciona 100% offline — lee datos de data/*.json

Ejecutar con: streamlit run app/main.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spotify Music Intelligence",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data loaders ──────────────────────────────────────────────────────────────

@st.cache_data
def load_tracks() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_tracks.json"
    if not path.exists():
        st.error(f"Data file not found: {path}\nRun `python data/generate_data.py` first.")
        return pd.DataFrame()
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df


@st.cache_data
def load_albums() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_albums.json"
    if not path.exists():
        return pd.DataFrame()
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df


@st.cache_data
def load_stats() -> dict:
    path = DATA_DIR / "radiohead_stats.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎵 Spotify Music Intelligence")
    st.markdown("**Radiohead — Audio Feature & Lyrics Analysis**")
    st.divider()
    st.markdown("**Navegación**")
    st.markdown("Use el menú de páginas de arriba ↑")
    st.divider()
    stats = load_stats()
    if stats:
        st.metric("Artista", stats.get("artist", "Radiohead"))
        st.metric("Álbumes de estudio", stats.get("total_albums", 7))
        st.metric("Total pistas", stats.get("total_tracks", 87))
        yr = stats.get("year_range", [1993, 2016])
        st.metric("Período", f"{yr[0]}–{yr[1]}")
    st.divider()
    st.caption("Audio: Spotify 1.2M Songs Dataset (Kaggle)")
    st.caption("Letras: lyrics.ovh (en tiempo real)")

# ── Home page ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
        padding: 2rem 2.5rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    ">
        <h1 style="color: white; margin: 0; font-size: 2.2rem;">
            🎵 Spotify Music Intelligence
        </h1>
        <p style="color: #b3b3b3; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            Análisis de audio features y letras de Radiohead · Práctica universitaria
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ## Descripción del Proyecto

    Sistema de análisis musical que explora la discografía de estudio de **Radiohead**
    usando el dataset *Spotify 1.2M+ Songs* de Kaggle y letras de **lyrics.ovh**.

    ### Qué incluye esta app

    | Página | Puntos | Contenido |
    |--------|--------|-----------|
    | 📀 Album Catalogue | 2 pts | Filtrado de álbumes de estudio + algoritmo explicado + timeline |
    | 🎛️ Audio Features | — | Evolución de features, scatter, heatmap, estadísticas por álbum |
    | 📝 Análisis de Letras | 4 pts | Letras en vivo (lyrics.ovh), nº palabras, top frecuencias |
    | 🔊 Artist Profile | — | Radar chart, comparativa de eras, perfil sonoro |

    ### Requisitos académicos cubiertos

    - ✅ **Requisito 1 — Filtrado de álbumes** (2 pts): 7 álbumes de estudio de Radiohead
    - ✅ **Requisito 2 — Análisis de letras** (4 pts): lyrics.ovh, nº palabras, top frecuencias
    - ✅ **Requisito 3 — Web app** (4 pts): Streamlit + Plotly, 4 páginas

    ### Fuente de datos

    Dataset audio: [Spotify 1.2M+ Songs — Kaggle](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)
    Letras: [lyrics.ovh](https://lyrics.ovh) (sin API key)
    Artista: **Radiohead** · Discografía: [Wikipedia](https://en.wikipedia.org/wiki/Radiohead_discography)
    """)

with col2:
    tracks_df = load_tracks()
    albums_df = load_albums()

    if not tracks_df.empty and not albums_df.empty:
        st.markdown("### Resumen de la discografía")

        # Album list
        album_summary = albums_df[["name", "year", "total_tracks"]].copy()
        album_summary.columns = ["Álbum", "Año", "Pistas"]
        st.dataframe(album_summary, use_container_width=True, hide_index=True)

        st.markdown("### Mean audio features")
        feat_names = ["energy", "danceability", "valence", "acousticness", "instrumentalness"]
        feat_vals = [round(tracks_df[f].mean(), 3) for f in feat_names]
        for name, val in zip(feat_names, feat_vals):
            st.progress(val, text=f"{name.title()}: {val:.3f}")
    else:
        st.warning("Data files not found. Run `python data/generate_data.py` to generate them.")
