"""
spotify-music-intelligence · app/components/header.py
Reusable page header component for the Streamlit application.
"""

from __future__ import annotations

import streamlit as st


def render_header(
    title: str = "Spotify Music Intelligence",
    subtitle: str = "NLP-powered music analytics",
    icon: str = "🎵",
) -> None:
    """Render a styled page header with title, subtitle, and decorative divider.

    Args:
        title: Main heading text.
        subtitle: Secondary description line.
        icon: Emoji icon displayed before the title.
    """
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        ">
            <h1 style="color: white; margin: 0; font-size: 2rem;">
                {icon} {title}
            </h1>
            <p style="color: #b3b3b3; margin: 0.3rem 0 0 0; font-size: 1rem;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
