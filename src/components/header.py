"""
Header Components - macOS Style
Clean, minimal headers inspired by macOS applications
"""

import streamlit as st
from src.ui.macos_design_system import COLORS, SPACING


def header_home():
    """Home screen header - centered logo and app name"""

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <style>
        .home-header {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: {SPACING['xxxl']};
            margin-top: {SPACING['xl']};
        }}

        .home-header img {{
            height: 80px;
            margin-bottom: {SPACING['md']};
        }}

        .home-header h1 {{
            font-size: 3rem !important;
            font-weight: 700 !important;
            color: {COLORS['text_primary']} !important;
            letter-spacing: -0.03em !important;
            margin: 0 !important;
            text-align: center;
        }}

        .home-header .tagline {{
            font-size: 1.125rem !important;
            font-weight: 400 !important;
            color: {COLORS['text_secondary']} !important;
            margin-top: {SPACING['sm']} !important;
            text-align: center;
        }}
        </style>

        <div class="home-header">
            <img src='{logo_url}' alt='SnapClass Logo' />
            <h1>SnapClass</h1>
            <p class="tagline">AI-powered attendance made simple</p>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    """Dashboard header - compact horizontal logo with app name"""

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <style>
        .dashboard-header {{
            display: flex;
            align-items: center;
            gap: {SPACING['md']};
            padding: {SPACING['sm']} 0;
        }}

        .dashboard-header img {{
            height: 48px;
            width: 48px;
        }}

        .dashboard-header .app-name {{
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            letter-spacing: -0.02em !important;
            margin: 0 !important;
            line-height: 1 !important;
        }}

        .dashboard-header .app-name-sub {{
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            color: {COLORS['text_secondary']} !important;
            text-transform: uppercase;
            letter-spacing: 0.05em !important;
            margin: 0 !important;
        }}
        </style>

        <div class="dashboard-header">
            <img src='{logo_url}' alt='SnapClass' />
            <div>
                <div class="app-name">SnapClass</div>
                <div class="app-name-sub">Attendance</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
