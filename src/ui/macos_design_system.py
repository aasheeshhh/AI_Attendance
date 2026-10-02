"""
macOS Design System for AI Attendance Application
Centralized styling inspired by Apple's macOS interface
"""

import streamlit as st

# ============================================================
# MACOS COLOR PALETTE
# ============================================================

COLORS = {
    # Backgrounds
    'background': '#F5F5F7',
    'surface_primary': '#FFFFFF',
    'surface_secondary': '#F2F2F7',
    'surface_tertiary': '#E5E5EA',

    # Text
    'text_primary': '#1D1D1F',
    'text_secondary': '#6E6E73',
    'text_tertiary': '#86868B',

    # Apple Blue
    'blue': '#007AFF',
    'blue_hover': '#0051D5',
    'blue_light': '#E3F2FF',

    # Status Colors
    'success': '#34C759',
    'warning': '#FF9F0A',
    'danger': '#FF3B30',

    # Borders
    'border': 'rgba(0, 0, 0, 0.08)',
    'border_medium': 'rgba(0, 0, 0, 0.12)',
    'border_strong': 'rgba(0, 0, 0, 0.18)',

    # Overlays
    'overlay': 'rgba(0, 0, 0, 0.4)',
}

# ============================================================
# TYPOGRAPHY
# ============================================================

TYPOGRAPHY = """
    -apple-system,
    BlinkMacSystemFont,
    "SF Pro Display",
    "SF Pro Text",
    "Helvetica Neue",
    Arial,
    sans-serif
"""

# ============================================================
# SPACING
# ============================================================

SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '12px',
    'lg': '16px',
    'xl': '24px',
    'xxl': '32px',
    'xxxl': '48px',
}

# ============================================================
# SHADOWS
# ============================================================

SHADOWS = {
    'sm': '0 1px 3px rgba(0, 0, 0, 0.06)',
    'md': '0 2px 8px rgba(0, 0, 0, 0.08)',
    'lg': '0 4px 16px rgba(0, 0, 0, 0.10)',
}

# ============================================================
# BORDER RADIUS
# ============================================================

RADIUS = {
    'sm': '6px',
    'md': '8px',
    'lg': '12px',
    'xl': '16px',
}


def apply_macos_base_styles():
    """Apply the foundational macOS design system styles"""

    st.markdown(f"""
        <style>
        /* ============================================================ */
        /* IMPORT SF PRO FONT (FALLBACK TO SYSTEM) */
        /* ============================================================ */

        * {{
            font-family: {TYPOGRAPHY};
        }}

        /* ============================================================ */
        /* HIDE STREAMLIT BRANDING */
        /* ============================================================ */

        #MainMenu, footer, header {{
            visibility: hidden;
        }}

        /* ============================================================ */
        /* BASE APP LAYOUT */
        /* ============================================================ */

        .stApp {{
            background: {COLORS['background']} !important;
        }}

        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }}

        /* ============================================================ */
        /* TYPOGRAPHY HIERARCHY */
        /* ============================================================ */

        h1 {{
            font-size: 2.5rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            letter-spacing: -0.02em !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }}

        h2 {{
            font-size: 1.75rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            letter-spacing: -0.01em !important;
            line-height: 1.3 !important;
            margin-bottom: 0.5rem !important;
        }}

        h3 {{
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.4 !important;
            margin-bottom: 0.5rem !important;
        }}

        p, div, span, label {{
            font-size: 0.9375rem !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.5 !important;
        }}

        /* Secondary text */
        .text-secondary {{
            color: {COLORS['text_secondary']} !important;
        }}

        /* ============================================================ */
        /* BUTTONS - MACOS STYLE */
        /* ============================================================ */

        /* Primary Button (Apple Blue) */
        button[kind="primary"] {{
            background: {COLORS['blue']} !important;
            color: white !important;
            border: none !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
            box-shadow: none !important;
        }}

        button[kind="primary"]:hover {{
            background: {COLORS['blue_hover']} !important;
            transform: translateY(-1px) !important;
            box-shadow: {SHADOWS['sm']} !important;
        }}

        button[kind="primary"]:active {{
            transform: translateY(0) !important;
            box-shadow: none !important;
        }}

        /* Secondary Button (Neutral) */
        button[kind="secondary"] {{
            background: {COLORS['surface_secondary']} !important;
            color: {COLORS['text_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
            box-shadow: none !important;
        }}

        button[kind="secondary"]:hover {{
            background: {COLORS['surface_tertiary']} !important;
            border-color: {COLORS['border_medium']} !important;
            transform: translateY(-1px) !important;
        }}

        /* Tertiary/Destructive Button */
        button[kind="tertiary"] {{
            background: transparent !important;
            color: {COLORS['danger']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
        }}

        button[kind="tertiary"]:hover {{
            background: rgba(255, 59, 48, 0.08) !important;
            border-color: {COLORS['danger']} !important;
        }}

        /* Default Button */
        button {{
            background: {COLORS['surface_primary']} !important;
            color: {COLORS['text_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
        }}

        button:hover {{
            background: {COLORS['surface_secondary']} !important;
            border-color: {COLORS['border_medium']} !important;
        }}

        /* Disabled state */
        button:disabled {{
            opacity: 0.4 !important;
            cursor: not-allowed !important;
        }}

        /* ============================================================ */
        /* INPUTS - MACOS STYLE */
        /* ============================================================ */

        input, textarea, .stTextInput input, .stTextArea textarea {{
            background: {COLORS['surface_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 12px !important;
            font-size: 0.9375rem !important;
            color: {COLORS['text_primary']} !important;
            transition: all 0.15s ease !important;
        }}

        input:focus, textarea:focus, .stTextInput input:focus {{
            border-color: {COLORS['blue']} !important;
            box-shadow: 0 0 0 3px {COLORS['blue_light']} !important;
            outline: none !important;
        }}

        /* ============================================================ */
        /* SELECT / DROPDOWN */
        /* ============================================================ */

        .stSelectbox > div > div {{
            background: {COLORS['surface_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
        }}

        /* ============================================================ */
        /* CARDS & CONTAINERS */
        /* ============================================================ */

        [data-testid="stContainer"] {{
            background: {COLORS['surface_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['lg']} !important;
            padding: {SPACING['lg']} !important;
        }}

        /* ============================================================ */
        /* DIVIDERS */
        /* ============================================================ */

        hr {{
            border: none !important;
            border-top: 1px solid {COLORS['border']} !important;
            margin: {SPACING['lg']} 0 !important;
        }}

        /* ============================================================ */
        /* DATAFRAME / TABLES */
        /* ============================================================ */

        .stDataFrame {{
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            overflow: hidden !important;
        }}

        /* ============================================================ */
        /* CAMERA INPUT */
        /* ============================================================ */

        [data-testid="stCameraInput"] {{
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['lg']} !important;
            overflow: hidden !important;
        }}

        /* ============================================================ */
        /* TRANSITIONS */
        /* ============================================================ */

        * {{
            transition-duration: 0.15s !important;
            transition-timing-function: ease !important;
        }}

        </style>
    """, unsafe_allow_html=True)


def apply_macos_window_shell():
    """Apply macOS-style window chrome/shell at the top"""

    st.markdown(f"""
        <style>
        /* macOS Traffic Lights - Visual Only */
        .macos-window-controls {{
            position: fixed;
            top: 12px;
            left: 12px;
            display: flex;
            gap: 8px;
            z-index: 1000;
        }}

        .macos-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            opacity: 0.8;
        }}

        .macos-dot.close {{ background: #FF5F56; }}
        .macos-dot.minimize {{ background: #FFBD2E; }}
        .macos-dot.maximize {{ background: #27C93F; }}

        </style>

        <div class="macos-window-controls">
            <div class="macos-dot close"></div>
            <div class="macos-dot minimize"></div>
            <div class="macos-dot maximize"></div>
        </div>
    """, unsafe_allow_html=True)
