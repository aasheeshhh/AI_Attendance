"""
Subject Card Component - macOS Style
Clean, compact card inspired by macOS Finder/Notes list items
"""

from html import escape
import streamlit as st
from src.ui.macos_design_system import COLORS, SPACING, RADIUS, SHADOWS


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Render a subject/course card in macOS style"""

    name = escape(str(name))
    code = escape(str(code))
    section = escape(str(section))

    st.markdown(f"""
        <style>
        .macos-subject-card {{
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['lg']};
            padding: {SPACING['lg']};
            margin-bottom: {SPACING['md']};
            transition: all 0.15s ease;
            box-shadow: {SHADOWS['sm']};
        }}

        .macos-subject-card:hover {{
            border-color: {COLORS['border_medium']};
            box-shadow: {SHADOWS['md']};
        }}

        .subject-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: {SPACING['sm']};
        }}

        .subject-title {{
            font-size: 1.125rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            margin: 0 !important;
        }}

        .subject-meta {{
            display: flex;
            gap: {SPACING['sm']};
            align-items: center;
            margin-bottom: {SPACING['md']};
        }}

        .subject-code-badge {{
            background: {COLORS['surface_secondary']};
            color: {COLORS['text_secondary']};
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            padding: 2px 8px;
            border-radius: {RADIUS['sm']};
            font-family: monospace !important;
        }}

        .subject-section {{
            font-size: 0.8125rem !important;
            color: {COLORS['text_tertiary']} !important;
        }}

        .subject-stats {{
            display: flex;
            gap: {SPACING['md']};
            padding-top: {SPACING['sm']};
            border-top: 1px solid {COLORS['border']};
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: {SPACING['xs']};
            font-size: 0.8125rem !important;
            color: {COLORS['text_secondary']} !important;
        }}

        .stat-value {{
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
        }}
        </style>

        <div class="macos-subject-card">
            <div class="subject-header">
                <div class="subject-title">{name}</div>
            </div>
            <div class="subject-meta">
                <span class="subject-code-badge">{code}</span>
                <span class="subject-section">Section {section}</span>
            </div>
    """, unsafe_allow_html=True)

    if stats:
        stats_html = '<div class="subject-stats">'
        for icon, label, value in stats:
            stats_html += f"""
                <div class="stat-item">
                    <span>{escape(str(icon))}</span>
                    <span class="stat-value">{escape(str(value))}</span>
                    <span>{escape(str(label))}</span>
                </div>
            """
        stats_html += '</div>'
        st.markdown(stats_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
