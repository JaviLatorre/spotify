"""
Página 4 — Perfil Sonoro del Artista
Comparativa de eras/épocas usando datos locales.
Radar chart, evolución temporal, comparativa entre álbumes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Artist Profile", page_icon="📊", layout="wide")

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

RADAR_FEATS = ["energy", "danceability", "valence", "acousticness",
               "instrumentalness", "liveness", "speechiness"]

ERAS = {
    "Debut (1993–1995)": ["Pablo Honey", "The Bends"],
    "Era dorada (1997–2001)": ["OK Computer", "Kid A", "Amnesiac"],
    "Última etapa (2007–2016)": ["In Rainbows", "A Moon Shaped Pool"],
}

# ── Data loaders ──────────────────────────────────────────────────────────────

@st.cache_data
def load_tracks() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_tracks.json"
    return pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))

@st.cache_data
def load_albums() -> pd.DataFrame:
    path = DATA_DIR / "radiohead_albums.json"
    return pd.DataFrame(json.loads(path.read_text(encoding="utf-8")))

@st.cache_data
def load_stats() -> dict:
    path = DATA_DIR / "radiohead_stats.json"
    return json.loads(path.read_text(encoding="utf-8"))

# ── Page ──────────────────────────────────────────────────────────────────────

st.title("📊 Perfil Sonoro del Artista")
st.caption("Radiohead — análisis de eras, radar chart y comparativas de álbumes")

tracks_df = load_tracks()
albums_df = load_albums()
stats = load_stats()

if tracks_df.empty:
    st.error("Data not found. Run `python data/generate_data.py` first.")
    st.stop()

album_order = albums_df.sort_values("year")["name"].tolist()

# ── Overview strip ────────────────────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🎤 Artista", "Radiohead")
col2.metric("💿 Álbumes estudio", stats.get("total_albums", 7))
col3.metric("🎵 Total pistas", stats.get("total_tracks", 87))
yr = stats.get("year_range", [1993, 2016])
col4.metric("📅 Inicio carrera", yr[0])
col5.metric("📅 Último álbum", yr[1])

st.divider()

# ── Section 1: Radar general ──────────────────────────────────────────────────
st.subheader("Radar — Perfil sonoro global vs por era")

global_means = {f: round(float(tracks_df[f].mean()), 4) for f in RADAR_FEATS}
era_means: dict[str, dict[str, float]] = {}
for era_label, era_albums in ERAS.items():
    era_df = tracks_df[tracks_df["album"].isin(era_albums)]
    era_means[era_label] = {f: round(float(era_df[f].mean()), 4) for f in RADAR_FEATS}

fig_radar = go.Figure()
palette = ["#1DB954", "#1E90FF", "#FF6B6B", "#F4D03F"]

# Global profile
vals_g = [global_means[f] for f in RADAR_FEATS]
fig_radar.add_trace(go.Scatterpolar(
    r=vals_g + [vals_g[0]],
    theta=RADAR_FEATS + [RADAR_FEATS[0]],
    mode="lines+markers",
    name="Global (todos los álbumes)",
    line={"color": "#FFFFFF", "width": 3, "dash": "dash"},
    fill="toself",
    fillcolor="rgba(255,255,255,0.05)",
))

for i, (era_label, feats) in enumerate(era_means.items()):
    vals = [feats[f] for f in RADAR_FEATS]
    fig_radar.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=RADAR_FEATS + [RADAR_FEATS[0]],
        mode="lines+markers",
        name=era_label,
        line={"color": palette[i % len(palette)], "width": 2},
        fill="toself",
        fillcolor=palette[i % len(palette)],
        opacity=0.20,
    ))

fig_radar.update_layout(
    polar={"radialaxis": {"visible": True, "range": [0, 1]}},
    title="Perfil sonoro por era musical — Radiohead",
    legend={"orientation": "h", "y": -0.15},
    height=520,
    paper_bgcolor="#0e1117",
    font={"color": "white"},
)
st.plotly_chart(fig_radar, use_container_width=True)

st.divider()

# ── Section 2: Feature evolution timeline ──────────────────────────────────────
st.subheader("Evolución de features a lo largo de la discografía")

col_f1, col_f2 = st.columns([1, 3])
with col_f1:
    evo_feats = st.multiselect(
        "Features",
        RADAR_FEATS,
        default=["energy", "valence", "acousticness"],
        key="evo_04",
    )

if evo_feats:
    album_feat_means = (
        tracks_df.groupby(["year", "album"])[evo_feats]
        .mean()
        .reset_index()
        .sort_values("year")
    )

    fig_evo = go.Figure()
    for i, feat in enumerate(evo_feats):
        fig_evo.add_trace(go.Scatter(
            x=album_feat_means["album"],
            y=album_feat_means[feat],
            mode="lines+markers",
            name=feat.title(),
            line={"color": palette[i % len(palette)], "width": 2},
            marker={"size": 10},
        ))

    fig_evo.update_layout(
        title="Evolución de features por álbum de estudio",
        xaxis={"categoryorder": "array", "categoryarray": album_order, "tickangle": -25},
        yaxis={"range": [0, 1]},
        legend={"orientation": "h", "y": -0.2},
        height=420,
        xaxis_rangeslider_visible=False,
    )
    st.plotly_chart(fig_evo, use_container_width=True)

st.divider()

# ── Section 3: Comparativa entre dos álbumes ──────────────────────────────────
st.subheader("Comparativa directa entre álbumes")

col_a, col_b = st.columns(2)
with col_a:
    alb_a = st.selectbox("Álbum A", album_order, index=0, key="alb_a")
with col_b:
    default_b = min(5, len(album_order) - 1) if len(album_order) > 1 else 0
    alb_b = st.selectbox("Álbum B", album_order, index=default_b, key="alb_b")

if alb_a != alb_b:
    a_means = tracks_df[tracks_df["album"] == alb_a][RADAR_FEATS].mean()
    b_means = tracks_df[tracks_df["album"] == alb_b][RADAR_FEATS].mean()

    # Radar comparison
    fig_cmp = go.Figure()
    for label, means, color in [(alb_a, a_means, "#1DB954"), (alb_b, b_means, "#1E90FF")]:
        vals = means.tolist()
        fig_cmp.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=RADAR_FEATS + [RADAR_FEATS[0]],
            mode="lines+markers",
            name=label,
            line={"color": color, "width": 2},
            fill="toself",
            fillcolor=color,
            opacity=0.25,
        ))
    fig_cmp.update_layout(
        polar={"radialaxis": {"visible": True, "range": [0, 1]}},
        title=f"Comparativa: {alb_a} vs {alb_b}",
        height=460,
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Difference bar chart
    diff = (a_means - b_means).sort_values()
    diff_df = diff.reset_index()
    diff_df.columns = ["Feature", "Diferencia (A - B)"]
    diff_df["Color"] = diff_df["Diferencia (A - B)"].apply(lambda v: "#1DB954" if v > 0 else "#e74c3c")

    fig_diff = px.bar(
        diff_df,
        x="Feature",
        y="Diferencia (A - B)",
        color="Color",
        color_discrete_map="identity",
        title=f"Diferencia de features: {alb_a} − {alb_b}",
        labels={"Feature": "Feature", "Diferencia (A - B)": "Diferencia"},
    )
    fig_diff.add_hline(y=0, line_dash="dash", line_color="white", line_width=1)
    fig_diff.update_layout(showlegend=False, height=360)
    st.plotly_chart(fig_diff, use_container_width=True)

    # Table
    cmp_table = pd.DataFrame({
        "Feature": RADAR_FEATS,
        alb_a: a_means.round(4).values,
        alb_b: b_means.round(4).values,
        "Diferencia (A−B)": (a_means - b_means).round(4).values,
    })
    st.dataframe(cmp_table, use_container_width=True, hide_index=True)
else:
    st.info("Selecciona dos álbumes distintos para comparar.")

st.divider()

# ── Section 4: Era comparison bar chart ──────────────────────────────────────────
st.subheader("Comparativa de eras musicales")

era_rows = []
for era_label, feats in era_means.items():
    for feat, val in feats.items():
        era_rows.append({"Era": era_label, "Feature": feat.title(), "Valor": val})

era_df = pd.DataFrame(era_rows)

fig_era = px.bar(
    era_df,
    x="Feature",
    y="Valor",
    color="Era",
    barmode="group",
    title="Audio features medios por era musical",
    color_discrete_sequence=["#1DB954", "#1E90FF", "#FF6B6B"],
    labels={"Feature": "Feature", "Valor": "Valor medio", "Era": "Era"},
)
fig_era.update_layout(
    xaxis_tickangle=-20,
    legend={"orientation": "h", "y": -0.2},
    height=420,
)
st.plotly_chart(fig_era, use_container_width=True)

st.divider()

# ── Section 5: Album cards ────────────────────────────────────────────────────
st.subheader("Resumen por álbum")

n_cols = 4
rows = [album_order[i:i+n_cols] for i in range(0, len(album_order), n_cols)]

for row_albums in rows:
    cols = st.columns(len(row_albums))
    for col, alb_name in zip(cols, row_albums):
        alb_row = albums_df[albums_df["name"] == alb_name]
        if alb_row.empty:
            continue
        alb_row = alb_row.iloc[0]
        alb_tracks = tracks_df[tracks_df["album"] == alb_name]
        with col:
            st.markdown(f"**{alb_name}**")
            st.caption(f"{int(alb_row['year'])} · {int(alb_row['total_tracks'])} pistas")
            for feat in ["energy", "valence", "acousticness"]:
                val = float(alb_tracks[feat].mean())
                st.progress(val, text=f"{feat.title()}: {val:.2f}")
