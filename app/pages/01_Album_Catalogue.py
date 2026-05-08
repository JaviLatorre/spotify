"""
Página 1 — Catálogo de Álbumes de Estudio
REQUISITO 1 (2 puntos): Filtrado de álbumes — explicación + antes/después.
Artista: Radiohead. Discografía de referencia:
https://en.wikipedia.org/wiki/Radiohead_discography
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Album Catalogue", page_icon="📀", layout="wide")

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

# ── Load data ─────────────────────────────────────────────────────────────────

@st.cache_data
def load_albums() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_albums.json"
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df

@st.cache_data
def load_tracks() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_tracks.json"
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df

# ── Page header ───────────────────────────────────────────────────────────────

st.title("📀 Catálogo de Álbumes de Estudio")
st.caption("Requisito 1 — Filtrado de álbumes (2 puntos) · Radiohead")

albums_df = load_albums()
tracks_df = load_tracks()

if albums_df.empty:
    st.error("Data not found. Run `python data/generate_data.py` first.")
    st.stop()

# ── Metrics row ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("💿 Álbumes de estudio", len(albums_df))
c2.metric("🎵 Total pistas", len(tracks_df))
c3.metric("📅 Primer álbum", albums_df["year"].min())
c4.metric("📅 Último álbum", albums_df["year"].max())

st.divider()

# ── Filtering explanation ─────────────────────────────────────────────────────
with st.expander("📋 Algoritmo de filtrado de álbumes de estudio", expanded=True):
    st.markdown("""
    ### Por qué filtramos álbumes

    El dataset de Spotify incluye **todo** lo publicado por un artista: compilaciones,
    singles, ediciones en vivo, EPs, remasterizaciones y caras B.
    Para un análisis riguroso necesitamos solo los **álbumes de estudio originales**.

    Referencia: [Radiohead — Wikipedia Discography](https://en.wikipedia.org/wiki/Radiohead_discography)

    ### Criterios de exclusión aplicados (4 pasos)

    | Paso | Criterio | Qué excluye |
    |------|----------|-------------|
    | 1 | `album_type != 'album'` | Singles, EPs, compilaciones marcadas por Spotify |
    | 2 | Keyword en el título | *live, compilation, reissue, deluxe, edition, remix, remaster, greatest hits, b-sides, collector…* |
    | 3 | `total_tracks < 5` | Mini-álbumes y EPs no clasificados |
    | 4 | Deduplicación | Remasters del mismo álbum → conservar versión más antigua |

    ### Antes vs. Después del filtrado (Radiohead)

    | Estado | Ítems en dataset |
    |--------|-----------------|
    | **Sin filtrar** | ~30 ítems (álbumes + compilaciones + singles + reissues) |
    | **Filtrados (estudio)** | **7 álbumes de estudio** |

    Los 7 álbumes coinciden con la discografía oficial de Wikipedia:
    *Pablo Honey* (1993), *The Bends* (1995), *OK Computer* (1997),
    *Kid A* (2000), *Amnesiac* (2001), *In Rainbows* (2007), *A Moon Shaped Pool* (2016).
    """)

    excluded_items = [
        ("Pablo Honey (Collector's Edition)",    "keyword 'edition' / reissue"),
        ("OK Computer OKNOTOK 1997 2017",        "keyword 'reissue' / compilation"),
        ("Kid A Mnesia (2021)",                  "keyword 'reissue' / box set"),
        ("I Might Be Wrong: Live Recordings",    "álbum en vivo (live)"),
        ("Com Lag (2+2=5)",                      "EP / album_type != album"),
        ("Drill EP (1992)",                      "EP / album_type != album"),
        ("The Best Of (2008)",                   "keyword 'best' / compilation"),
        ("My Iron Lung EP",                      "EP / total_tracks < 5"),
        ("Airbag/How Am I Driving?",             "EP / album_type != album"),
        ("In Rainbows Disk 2",                   "keyword 'disk' / extra content"),
        ("TKOL RMX 1234567",                     "keyword 'rmx' / remix"),
        ("Supercollider/The Butcher",            "single / album_type = single"),
    ]
    excl_df = pd.DataFrame(excluded_items, columns=["Ítem excluido", "Razón"])
    st.dataframe(excl_df, use_container_width=True, hide_index=True)

# ── Albums table ──────────────────────────────────────────────────────────────
st.subheader("Álbumes de estudio — Radiohead")

display_df = albums_df[["name", "release_date", "total_tracks", "album_type", "year"]].copy()
display_df["release_date"] = display_df["release_date"].dt.strftime("%Y-%m-%d")
display_df.columns = ["Álbum", "Fecha lanzamiento", "Pistas", "Tipo", "Año"]

st.dataframe(display_df, use_container_width=True, hide_index=True, height=220)

st.divider()

# ── Timeline chart ────────────────────────────────────────────────────────────
st.subheader("Timeline de lanzamientos")

fig_timeline = px.scatter(
    albums_df.sort_values("year"),
    x="year",
    y="name",
    size="total_tracks",
    color="total_tracks",
    hover_name="name",
    hover_data={"total_tracks": True, "release_date": True, "year": False},
    title="Discografía de estudio — Radiohead",
    color_continuous_scale="Viridis",
    size_max=50,
    labels={"year": "Año", "name": "Álbum", "total_tracks": "Pistas"},
)
fig_timeline.update_layout(
    height=320,
    yaxis={"categoryorder": "total ascending"},
    showlegend=False,
    coloraxis_showscale=False,
)
st.plotly_chart(fig_timeline, use_container_width=True)

# ── Track distribution chart ──────────────────────────────────────────────────
col_bar, col_pie = st.columns(2)

with col_bar:
    st.subheader("Pistas por álbum")
    fig_bar = px.bar(
        albums_df.sort_values("year"),
        x="name",
        y="total_tracks",
        color="year",
        hover_name="name",
        title="Número de pistas por álbum de estudio",
        color_continuous_scale="Plasma",
        labels={"name": "Álbum", "total_tracks": "Pistas", "year": "Año"},
    )
    fig_bar.update_layout(xaxis_tickangle=-20, showlegend=False, height=360)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    st.subheader("Distribución de pistas")
    fig_pie = px.pie(
        albums_df,
        names="name",
        values="total_tracks",
        title="Proporción de pistas por álbum",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_pie.update_layout(height=360)
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Album details ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("Detalle por álbum")

selected_album = st.selectbox(
    "Selecciona un álbum",
    albums_df["name"].tolist(),
    key="album_sel_01",
)

if selected_album:
    album_row = albums_df[albums_df["name"] == selected_album].iloc[0]
    album_tracks = tracks_df[tracks_df["album"] == selected_album].copy()

    ca, cb, cc = st.columns(3)
    ca.metric("Pistas", int(album_row["total_tracks"]))
    cb.metric("Año", int(album_row["year"]))
    cc.metric("Duración media", f"{album_tracks['duration_min'].mean():.1f} min")

    show_cols = ["track_number", "name", "duration_min", "energy", "valence", "danceability"]
    album_tracks_display = album_tracks[show_cols].copy()
    album_tracks_display.columns = ["#", "Canción", "Duración (min)", "Energía", "Valencia", "Bailabilidad"]
    st.dataframe(album_tracks_display.sort_values("#"), use_container_width=True, hide_index=True)
