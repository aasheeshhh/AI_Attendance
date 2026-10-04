"""
Reference-Inspired Design System for AI Attendance
Based on pixel-perfect-snap-8916 visual language

This is an ENHANCED version of the existing macOS design system,
incorporating the refined visual language from the reference project.
"""

import streamlit as st

# ============================================================
# ENHANCED COLOR PALETTE (OKLCH-inspired values in hex)
# ============================================================

COLORS = {
    # Backgrounds - Gradient-capable
    'background': '#F5F5F7',  # oklch(0.97 0.002 286)
    'background_gradient_start': '#F0EFF5',  # Subtle purple tint
    'background_gradient_end': '#F5F7FA',  # Subtle blue tint

    # Surfaces with sophisticated shadows
    'surface_primary': '#FFFFFF',
    'surface_secondary': '#F2F2F7',
    'surface_tertiary': '#E5E5EA',
    'surface_glass': 'rgba(255, 255, 255, 0.7)',  # Frosted glass

    # Text hierarchy
    'text_primary': '#1D1D1F',
    'text_secondary': '#6E6E73',
    'text_tertiary': '#86868B',

    # Apple Blue (primary action color)
    'blue': '#007AFF',
    'blue_hover': '#0051D5',
    'blue_light': 'rgba(0, 122, 255, 0.1)',

    # Status Colors
    'success': '#34C759',
    'warning': '#FF9F0A',
    'danger': '#FF3B30',

    # Borders - More refined
    'border': 'rgba(0, 0, 0, 0.06)',
    'border_medium': 'rgba(0, 0, 0, 0.07)',
    'border_strong': 'rgba(0, 0, 0, 0.12)',

    # Accent hover states
    'accent_bg': 'rgba(0, 122, 255, 0.08)',
    'accent_fg': 'rgba(0, 122, 255, 1)',

    # Sidebar colors
    'sidebar_bg': 'rgba(245, 245, 247, 0.72)',
    'sidebar_accent': 'rgba(0, 0, 0, 0.06)',
}

# ============================================================
# TYPOGRAPHY (SF Pro System)
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
# SPACING SCALE
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
# SOPHISTICATED SHADOWS (Panel-based)
# ============================================================

SHADOWS = {
    # Panel shadows (refined, multi-layer)
    'panel': '0 0 0 0.5px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04), 0 8px 24px -12px rgba(0, 0, 0, 0.08)',
    'panel_hover': '0 0 0 0.5px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.04), 0 16px 36px -16px rgba(0, 0, 0, 0.14)',
    'window': '0 0 0 0.5px rgba(0, 0, 0, 0.12), 0 30px 80px -20px rgba(0, 0, 0, 0.22)',
    'control': '0 0 0 0.5px rgba(0, 0, 0, 0.1), 0 1px 1.5px rgba(0, 0, 0, 0.08)',
}

# ============================================================
# BORDER RADIUS
# ============================================================

RADIUS = {
    'sm': '6px',
    'md': '8px',
    'lg': '12px',
    'xl': '16px',
    'xxl': '22px',  # Panel radius
}


def apply_reference_design_system():
    """
    Apply the complete reference-inspired design system
    This enhances the existing macOS design with the reference's visual language
    """

    st.markdown(f"""
        <style>
        /* ============================================================ */
        /* ENHANCED TYPOGRAPHY & BASE */
        /* ============================================================ */

        * {{
            font-family: {TYPOGRAPHY};
        }}

        html {{
            -webkit-font-smoothing: antialiased;
        }}

        /* ============================================================ */
        /* GRADIENT DESKTOP BACKGROUND */
        /* ============================================================ */

        .stApp {{
            background: radial-gradient(1200px 600px at 10% -10%, {COLORS['background_gradient_start']}, transparent 60%),
                        radial-gradient(900px 500px at 100% 110%, {COLORS['background_gradient_end']}, transparent 60%),
                        {COLORS['background']};
            background-attachment: fixed;
        }}

        /* ============================================================ */
        /* HIDE STREAMLIT BRANDING */
        /* ============================================================ */

        #MainMenu, footer, header {{
            visibility: hidden;
        }}

        /* ============================================================ */
        /* BASE LAYOUT */
        /* ============================================================ */

        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1400px !important;
        }}

        /* ============================================================ */
        /* TYPOGRAPHY HIERARCHY (Enhanced) */
        /* ============================================================ */

        h1, h2, h3 {{
            letter-spacing: -0.02em !important;
        }}

        h1 {{
            font-size: 2.25rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.2 !important;
            margin-bottom: 0.5rem !important;
        }}

        h2 {{
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.3 !important;
            margin-bottom: 0.5rem !important;
        }}

        h3 {{
            font-size: 1.125rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.4 !important;
            margin-bottom: 0.5rem !important;
        }}

        p, div, span, label {{
            font-size: 0.9375rem !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.5 !important;
            letter-spacing: -0.005em !important;
        }}

        /* ============================================================ */
        /* PANEL-BASED CARDS (Reference Style) */
        /* ============================================================ */

        .panel {{
            background: {COLORS['surface_primary']};
            border-radius: {RADIUS['xxl']};
            box-shadow: {SHADOWS['panel']};
            transition: box-shadow 200ms ease, transform 200ms ease;
            padding: {SPACING['xl']};
            border: 1px solid {COLORS['border']};
        }}

        .panel:hover {{
            box-shadow: {SHADOWS['panel_hover']};
            transform: translateY(-1px);
        }}

        .panel-static {{
            background: {COLORS['surface_primary']};
            border-radius: {RADIUS['xxl']};
            box-shadow: {SHADOWS['panel']};
            padding: {SPACING['xl']};
            border: 1px solid {COLORS['border']};
        }}

        /* Glass effect panels */
        .glass-panel {{
            background: {COLORS['surface_glass']};
            backdrop-filter: blur(24px) saturate(180%);
            border-radius: {RADIUS['xl']};
            box-shadow: {SHADOWS['control']};
            padding: {SPACING['lg']};
            border: 1px solid {COLORS['border']};
        }}

        /* ============================================================ */
        /* ENHANCED BUTTONS */
        /* ============================================================ */

        /* Primary Button */
        button[kind="primary"], .stButton > button[kind="primary"] {{
            background: {COLORS['blue']} !important;
            color: white !important;
            border: none !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
            box-shadow: {SHADOWS['control']} !important;
        }}

        button[kind="primary"]:hover {{
            background: {COLORS['blue_hover']} !important;
            transform: translateY(-1px) !important;
            box-shadow: {SHADOWS['panel']} !important;
        }}

        button[kind="primary"]:active {{
            transform: translateY(0) !important;
        }}

        /* Secondary Button */
        button[kind="secondary"], .stButton > button[kind="secondary"] {{
            background: {COLORS['surface_primary']} !important;
            color: {COLORS['text_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 16px !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            transition: all 0.15s ease !important;
            box-shadow: {SHADOWS['control']} !important;
        }}

        button[kind="secondary"]:hover {{
            background: {COLORS['surface_secondary']} !important;
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

        /* ============================================================ */
        /* REFINED INPUTS */
        /* ============================================================ */

        input, textarea, .stTextInput input, .stTextArea textarea {{
            background: {COLORS['surface_primary']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 8px 12px !important;
            font-size: 0.9375rem !important;
            color: {COLORS['text_primary']} !important;
            transition: all 0.15s ease !important;
            box-shadow: {SHADOWS['control']} !important;
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
            box-shadow: {SHADOWS['control']} !important;
        }}

        /* ============================================================ */
        /* ENHANCED DATAFRAMES / TABLES */
        /* ============================================================ */

        .stDataFrame {{
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['lg']} !important;
            overflow: hidden !important;
            box-shadow: {SHADOWS['control']} !important;
        }}

        /* Table row hover */
        .stDataFrame tbody tr:hover {{
            background: {COLORS['surface_secondary']} !important;
        }}

        /* ============================================================ */
        /* PAGE TRANSITION ANIMATION */
        /* ============================================================ */

        .main .block-container {{
            animation: page-in 260ms cubic-bezier(0.2, 0.8, 0.2, 1);
        }}

        @keyframes page-in {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* ============================================================ */
        /* STAT CARDS (Reference Style) */
        /* ============================================================ */

        .stat-card {{
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['xl']};
            padding: {SPACING['lg']};
            box-shadow: {SHADOWS['panel']};
            transition: all 200ms ease;
        }}

        .stat-card:hover {{
            box-shadow: {SHADOWS['panel_hover']};
            transform: translateY(-1px);
        }}

        .stat-card-value {{
            font-size: 2rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            letter-spacing: -0.02em !important;
        }}

        .stat-card-label {{
            font-size: 0.8125rem !important;
            color: {COLORS['text_secondary']} !important;
            font-weight: 500 !important;
        }}

        .stat-card-hint {{
            font-size: 0.75rem !important;
            color: {COLORS['text_tertiary']} !important;
            margin-top: {SPACING['xs']};
        }}

        /* ============================================================ */
        /* DIVIDERS */
        /* ============================================================ */

        hr {{
            border: none !important;
            border-top: 1px solid {COLORS['border']} !important;
            margin: {SPACING['xl']} 0 !important;
        }}

        /* ============================================================ */
        /* CAMERA INPUT */
        /* ============================================================ */

        [data-testid="stCameraInput"] {{
            border: 1px solid {COLORS['border']} !important;
            border-radius: {RADIUS['xl']} !important;
            overflow: hidden !important;
            box-shadow: {SHADOWS['panel']} !important;
        }}

        /* ============================================================ */
        /* SMOOTH TRANSITIONS */
        /* ============================================================ */

        * {{
            transition-duration: 0.15s !important;
            transition-timing-function: ease !important;
        }}

        /* ============================================================ */
        /* AI SURFACE (Gradient for AI features) */
        /* ============================================================ */

        .ai-surface {{
            background: linear-gradient(135deg, rgba(0, 122, 255, 0.08), rgba(120, 200, 255, 0.05));
            border-radius: {RADIUS['lg']};
            padding: {SPACING['md']};
            border: 1px solid {COLORS['border']};
        }}

        </style>
    """, unsafe_allow_html=True)


def apply_sidebar_navigation(active_tab=None, tabs=None, on_tab_change=None):
    """
    Create a sidebar-style navigation inspired by the reference design
    This replaces the top tab navigation with a sidebar approach
    """

    if not tabs:
        return

    st.markdown(f"""
        <style>
        .sidebar-nav {{
            background: {COLORS['sidebar_bg']};
            backdrop-filter: blur(24px);
            border-radius: {RADIUS['xl']};
            padding: {SPACING['md']};
            border: 1px solid {COLORS['border']};
            margin-bottom: {SPACING['xl']};
        }}

        .sidebar-section-label {{
            font-size: 0.6875rem !important;
            font-weight: 500 !important;
            color: {COLORS['text_tertiary']} !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: {SPACING['sm']};
            padding-left: {SPACING['sm']};
        }}

        .sidebar-nav-item {{
            display: flex;
            align-items: center;
            gap: {SPACING['sm']};
            padding: {SPACING['sm']} {SPACING['md']};
            border-radius: {RADIUS['md']};
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: {COLORS['text_primary']} !important;
            cursor: pointer;
            transition: all 150ms ease;
            margin-bottom: 2px;
        }}

        .sidebar-nav-item:hover {{
            background: {COLORS['sidebar_accent']};
        }}

        .sidebar-nav-item.active {{
            background: {COLORS['accent_bg']};
            color: {COLORS['accent_fg']} !important;
            font-weight: 600 !important;
        }}

        .sidebar-nav-icon {{
            width: 16px;
            height: 16px;
        }}
        </style>
    """, unsafe_allow_html=True)


def create_page_header(title, subtitle=None, right_content=None):
    """
    Create a page header in the reference design style
    """

    st.markdown(f"""
        <style>
        .page-header {{
            margin-bottom: {SPACING['xl']};
        }}

        .page-header-title {{
            font-size: 1.75rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            letter-spacing: -0.02em !important;
            margin: 0 !important;
        }}

        .page-header-subtitle {{
            font-size: 0.875rem !important;
            color: {COLORS['text_secondary']} !important;
            margin-top: {SPACING['xs']};
        }}
        </style>

        <div class="page-header">
            <h1 class="page-header-title">{title}</h1>
            {f'<p class="page-header-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)
