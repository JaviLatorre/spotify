"""
Página 2 — Análisis de Features de Audio
Lee datos locales de data/radiohead_tracks.json y data/radiohead_albums.json.
REQUISITO 2 (4 puntos): evolución temporal, scatter, heatmap, estadísticas.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Audio Features", page_icon="🎛️", layout="wide")

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

FEATURE_COLS = ["energy", "danceability", "valence", "acousticness",
                "instrumentalness", "liveness", "speechiness"]

# ── Data loaders ──────────────────────────────────────────────────────────────

@st.cache_data
def load_tracks() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_tracks.json"
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    return df

@st.cache_data
def load_albums() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_albums.json"
    df = pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))
    return df

# ── Page header ───────────────────────────────────────────────────────────────

st.title("🎛️ Análisis de Features de Audio")
st.caption("Análisis de audio features · Radiohead")

tracks_df = load_tracks()
albums_df = load_albums()

if tracks_df.empty:
    st.error("Data not found. Run `python data/generate_data.py` first.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Filtros")
    st.divider()

    all_albums = sorted(tracks_df["album"].unique().tolist())
    selected_albums = st.multiselect(
        "Álbumes",
        all_albums,
        default=all_albums,
        key="albums_02",
    )

    selected_features = st.multiselect(
        "Features a mostrar",
        FEATURE_COLS,
        default=["energy", "danceability", "valence", "acousticness"],
        key="feat_02",
    )

    year_min = int(tracks_df["year"].min())
    year_max = int(tracks_df["year"].max())
    year_range = st.slider("Rango de años", year_min, year_max,
                           (year_min, year_max), key="yr_02")

# Apply filters
df = tracks_df[
    (tracks_df["album"].isin(selected_albums)) &
    (tracks_df["year"] >= year_range[0]) &
    (tracks_df["year"] <= year_range[1])
].copy()

if df.empty:
    st.warning("No hay datos con los filtros actuales.")
    st.stop()

# ── Metrics row ───────────────────────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)
c1.metric("🎵 Pistas", len(df))
c2.metric("⚡ Energía media", f"{df['energy'].mean():.3f}")
c3.metric("😊 Valencia media", f"{df['valence'].mean():.3f}")
c4.metric("💃 Bailabilidad media", f"{df['danceability'].mean():.3f}")

st.divider()

# ── Chart 1: Feature Evolution ────────────────────────────────────────────────
st.subheader("Evolución temporal de features (por álbum)")

if not selected_features:
    st.info("Selecciona al menos una feature en el sidebar.")
else:
    album_means = (
        df.groupby(["year", "album"])[selected_features]
        .mean()
        .reset_index()
    )
    album_order = albums_df.sort_values("year")["name"].tolist()

    fig_evo = go.Figure()
    palette = px.colors.qualitative.Plotly
    for i, feat in enumerate(selected_features):
        feat_df = album_means.sort_values("year")
        fig_evo.add_trace(go.Scatter(
            x=feat_df["album"],
            y=feat_df[feat],
            mode="lines+markers",
            name=feat.title(),
            line={"color": palette[i % len(palette)], "width": 2},
            marker={"size": 9},
            hovertemplate=f"<b>{feat.title()}</b><br>Álbum: %{{x}}<br>Valor: %{{y:.3f}}<extra></extra>",
        ))

    fig_evo.update_layout(
        title="Evolución de audio features por álbum de estudio",
        xaxis_title="Álbum (orden cronológico)",
        yaxis_title="Valor medio de feature",
        xaxis={"categoryorder": "array", "categoryarray": album_order, "tickangle": -30},
        legend={"orientation": "h", "y": -0.25},
        height=420,
    )
    st.plotly_chart(fig_evo, use_container_width=True)

st.divider()

# ── Chart 2: Scatter Plot ─────────────────────────────────────────────────────
st.subheader("Scatter Plot — Feature X vs Feature Y")

col_x, col_y, col_c = st.columns(3)
with col_x:
    feat_x = st.selectbox("Eje X", FEATURE_COLS, index=0, key="sx_02")
with col_y:
    feat_y = st.selectbox("Eje Y", FEATURE_COLS, index=2, key="sy_02")
with col_c:
    color_by = st.selectbox("Color por", ["album", "year"], index=0, key="sc_02")

fig_scatter = px.scatter(
    df,
    x=feat_x,
    y=feat_y,
    color=color_by,
    hover_name="name",
    hover_data={"album": True, "year": True, feat_x: ":.3f", feat_y: ":.3f"},
    title=f"{feat_x.title()} vs {feat_y.title()} — Radiohead",
    color_discrete_sequence=px.colors.qualitative.Set2
    if color_by == "album" else None,
    color_continuous_scale="Viridis" if color_by == "year" else None,
    labels={feat_x: feat_x.title(), feat_y: feat_y.title()},
)
fig_scatter.update_layout(height=450)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ── Chart 3: Heatmap features × álbum ────────────────────────────────────────
st.subheader("Heatmap — Features × Álbum")

heat_feats = selected_features if selected_features else FEATURE_COLS
album_feat_means = (
    df.groupby("album")[heat_feats]
    .mean()
    .reindex([a for a in album_order if a in df["album"].unique()])
)

fig_heat = px.imshow(
    album_feat_means.T,
    color_continuous_scale="RdYlGn",
    aspect="auto",
    title="Media de features por álbum (más verde = mayor valor)",
    labels={"x": "Álbum", "y": "Feature", "color": "Valor"},
    zmin=0, zmax=1,
)
fig_heat.update_xaxes(tickangle=-30)
fig_heat.update_layout(height=380)
st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# ── Chart 4: Boxplot distribución por álbum ───────────────────────────────────
st.subheader("Distribución de features por álbum")

col_box1, col_box2 = st.columns([1, 3])
with col_box1:
    box_feat = st.selectbox("Feature", FEATURE_COLS, index=0, key="bf_02")

fig_box = px.box(
    df.assign(album=pd.Categorical(df["album"], categories=album_order, ordered=True)).sort_values("album"),
    x="album",
    y=box_feat,
    color="album",
    title=f"Distribución de {box_feat.title()} por álbum",
    labels={"album": "Álbum", box_feat: box_feat.title()},
    points="all",
)
fig_box.update_layout(xaxis_tickangle=-30, showlegend=False, height=420)
st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# ── Stats table ───────────────────────────────────────────────────────────────
st.subheader("Estadísticas descriptivas de features")

stat_feats = selected_features if selected_features else FEATURE_COLS
stats_df = df[stat_feats].describe().round(4)
stats_df.index = ["Conteo", "Media", "Desv. estándar", "Mínimo",
                  "P25", "Mediana (P50)", "P75", "Máximo"]
st.dataframe(stats_df, use_container_width=True)

# Per-album stats
st.subheader("Media de features por álbum")
per_album = (
    df.groupby("album")[stat_feats]
    .mean()
    .round(4)
    .reset_index()
)
per_album.columns = ["Álbum"] + [f.title() for f in stat_feats]
st.dataframe(per_album, use_container_width=True, hide_index=True)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("🔍 Datos de pistas (filtrados)"):
    show_cols = ["name", "album", "year", "track_number", "duration_min"] + FEATURE_COLS
    st.dataframe(df[show_cols].sort_values(["year", "track_number"]),
                 use_container_width=True, hide_index=True)
