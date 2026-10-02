"""
Base Layout Styles for AI Attendance Application
Now using macOS Design System
"""

import streamlit as st
from src.ui.macos_design_system import apply_macos_base_styles, apply_macos_window_shell, COLORS, SPACING, RADIUS


def style_background_home():
    """Apply macOS-style background for home/landing screen"""

    st.markdown(f"""
        <style>
        /* Home screen uses a subtle gradient */
        .stApp {{
            background: linear-gradient(180deg, {COLORS['background']} 0%, #E8E8ED 100%) !important;
        }}

        /* Center the home portal cards */
        .home-portal-card {{
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['xl']};
            padding: {SPACING['xxl']};
            text-align: center;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }}

        .home-portal-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            border-color: {COLORS['blue']};
        }}

        /* Home specific column styling */
        .stApp div[data-testid="column"] {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    """Apply macOS-style background for dashboard screens"""

    st.markdown(f"""
        <style>
        /* Dashboard uses clean flat background */
        .stApp {{
            background: {COLORS['background']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    """Apply base macOS design system to entire app"""

    # Apply the core macOS design system
    apply_macos_base_styles()

    # Apply macOS window chrome
    apply_macos_window_shell()
