"""
Footer Components - macOS Style
Subtle, clean footers
"""

import streamlit as st
from src.ui.macos_design_system import COLORS, SPACING


def footer_home():
    """Home screen footer"""

    st.markdown(f"""
        <style>
        .macos-footer {{
            margin-top: {SPACING['xxxl']};
            padding-top: {SPACING['xl']};
            border-top: 1px solid {COLORS['border']};
            display: flex;
            justify-content: center;
            align-items: center;
            gap: {SPACING['sm']};
        }}

        .macos-footer p {{
            font-size: 0.8125rem !important;
            color: {COLORS['text_tertiary']} !important;
            margin: 0 !important;
        }}
        </style>

        <div class="macos-footer">
            <p>SnapClass • Designed for macOS</p>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    """Dashboard footer"""

    st.markdown(f"""
        <style>
        .macos-footer-dashboard {{
            margin-top: {SPACING['xxxl']};
            padding-top: {SPACING['lg']};
            border-top: 1px solid {COLORS['border']};
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .macos-footer-dashboard p {{
            font-size: 0.75rem !important;
            color: {COLORS['text_tertiary']} !important;
            margin: 0 !important;
        }}
        </style>

        <div class="macos-footer-dashboard">
            <p>SnapClass Attendance</p>
            <p>v1.0.0</p>
        </div>
    """, unsafe_allow_html=True)
