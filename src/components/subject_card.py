"""
Subject Card Component - Reference-Inspired macOS Style
Clean, refined panel cards matching pixel-perfect-snap-8916 design
"""

from html import escape
import streamlit as st
from src.ui.macos_design_system import COLORS, SPACING, RADIUS, SHADOWS


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Render a subject/course card in reference-inspired panel style"""

    name = escape(str(name))
    code = escape(str(code))
    section = escape(str(section))

    st.markdown(f"""
        <style>
        .subject-card {{
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['xxl']};
            padding: {SPACING['xl']};
            margin-bottom: {SPACING['lg']};
            transition: all 200ms ease;
            box-shadow: {SHADOWS['panel']};
        }}

        .subject-card:hover {{
            box-shadow: {SHADOWS['panel_hover']};
            transform: translateY(-1px);
        }}

        .subject-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: {SPACING['md']};
        }}

        .subject-title {{
            font-size: 1.125rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            margin: 0 !important;
            letter-spacing: -0.01em !important;
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
            font-weight: 600 !important;
            padding: 3px 10px;
            border-radius: {RADIUS['sm']};
            font-family: 'SF Mono', 'Menlo', monospace !important;
            letter-spacing: 0.02em;
            border: 1px solid {COLORS['border']};
        }}

        .subject-section {{
            font-size: 0.8125rem !important;
            color: {COLORS['text_tertiary']} !important;
            font-weight: 500 !important;
        }}

        .subject-stats {{
            display: flex;
            gap: {SPACING['lg']};
            padding-top: {SPACING['md']};
            border-top: 1px solid {COLORS['border']};
            margin-top: {SPACING['sm']};
        }}

        .stat-item {{
            display: flex;
            align-items: baseline;
            gap: {SPACING['xs']};
            font-size: 0.8125rem !important;
        }}

        .stat-icon {{
            font-size: 0.875rem;
            opacity: 0.8;
        }}

        .stat-value {{
            font-weight: 700 !important;
            color: {COLORS['text_primary']} !important;
            font-size: 1rem !important;
        }}

        .stat-label {{
            color: {COLORS['text_secondary']} !important;
            font-weight: 500 !important;
        }}
        </style>

        <div class="subject-card">
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
                    <span class="stat-icon">{escape(str(icon))}</span>
                    <span class="stat-value">{escape(str(value))}</span>
                    <span class="stat-label">{escape(str(label))}</span>
                </div>
            """
        stats_html += '</div>'
        st.markdown(stats_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if footer_callback:
        st.markdown(f"<div style='height: {SPACING['sm']};'></div>", unsafe_allow_html=True)
        footer_callback()
