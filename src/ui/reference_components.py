"""
Reference UI Components - Direct Transfer from pixel-perfect-snap-8916
Streamlit implementations matching the exact reference project structure
"""

import streamlit as st
from typing import Optional, List, Tuple, Callable, Literal

# Reference design tokens (from ui.tsx and global CSS)
REFERENCE_COLORS = {
    'background': 'oklch(0.97 0.002 286)',  # #F5F5F7
    'card': 'oklch(1 0 0)',  # Pure white
    'card_hover': 'oklch(1 0 0)',
    'popover': 'oklch(1 0 0 / 0.92)',
    'primary': 'oklch(0.22 0.004 286)',  # #1D1D1F
    'primary_foreground': 'oklch(0.98 0 0)',
    'secondary': 'oklch(0.955 0.003 286 / 0.72)',
    'secondary_foreground': 'oklch(0.22 0.004 286)',
    'muted': 'oklch(0.955 0.003 286)',
    'muted_foreground': 'oklch(0.53 0.008 286)',
    'accent': 'oklch(0.955 0.003 286 / 0.72)',
    'accent_foreground': 'oklch(0.22 0.004 286)',
    'destructive': 'oklch(0.64 0.22 27)',  # #FF3B30
    'destructive_foreground': 'oklch(0.98 0 0)',
    'border': 'oklch(0 0 0 / 0.06)',
    'input': 'oklch(0 0 0 / 0.06)',
    'ring': 'oklch(0.6 0.2 256)',  # Blue
    'success': 'oklch(0.66 0.17 150)',  # Green
    'warning': 'oklch(0.72 0.17 60)',  # Orange
    'sidebar_bg': 'oklch(0.955 0.003 286 / 0.72)',
}

REFERENCE_SHADOWS = {
    'panel': '0 0 0 0.5px oklch(0 0 0 / 0.06), 0 1px 2px oklch(0 0 0 / 0.04), 0 8px 24px -12px oklch(0 0 0 / 0.08)',
    'panel_hover': '0 0 0 0.5px oklch(0 0 0 / 0.07), 0 2px 4px oklch(0 0 0 / 0.04), 0 16px 36px -16px oklch(0 0 0 / 0.14)',
    'control': '0 0 0 0.5px oklch(0 0 0 / 0.1), 0 1px 1.5px oklch(0 0 0 / 0.08)',
}

REFERENCE_RADIUS = {
    'sm': '6px',
    'md': '8px',
    'lg': '10px',
    'xl': '12px',
    '2xl': '16px',
    '3xl': '22px',  # Panel radius
}


def apply_reference_base_styles():
    """Apply base reference design system styles - exact match to reference project"""

    st.markdown(f"""
        <style>
        /* Reset and base */
        * {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Hide Streamlit branding */
        #MainMenu, footer, header {{
            visibility: hidden;
        }}

        /* Desktop gradient background (exact reference) */
        .stApp {{
            background: radial-gradient(1200px 600px at 10% -10%, oklch(0.97 0.008 280), transparent 60%),
                        radial-gradient(900px 500px at 100% 110%, oklch(0.97 0.008 240), transparent 60%),
                        oklch(0.97 0.002 286) !important;
            background-attachment: fixed !important;
        }}

        .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}

        /* Typography matching reference */
        h1, h2, h3 {{
            letter-spacing: -0.02em !important;
        }}

        p, div, span {{
            letter-spacing: -0.005em !important;
        }}

        /* Page enter animation (260ms from reference) */
        .main .block-container {{
            animation: page-enter 260ms cubic-bezier(0.2, 0.8, 0.2, 1);
        }}

        @keyframes page-enter {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
    """, unsafe_allow_html=True)


def render_topbar(app_title: str = "AI Attendance", user_name: str = "User", user_role: str = "Teacher"):
    """
    Render TopBar exactly matching reference AppShell.tsx
    Height: 56px (h-14), Logo + Title + Search + Notifications + Avatar
    """

    initials = ''.join([part[0] for part in user_name.split()][:2]).upper()

    st.markdown(f"""
        <style>
        .ref-topbar {{
            position: sticky;
            top: 0;
            z-index: 50;
            height: 56px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            background: {REFERENCE_COLORS['card']};
            border-bottom: 1px solid {REFERENCE_COLORS['border']};
            backdrop-filter: blur(12px);
        }}

        .ref-topbar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .ref-logo {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: linear-gradient(135deg, oklch(0.6 0.2 256), oklch(0.7 0.18 280));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}

        .ref-app-title {{
            font-size: 15px;
            font-weight: 600;
            color: {REFERENCE_COLORS['primary']};
            letter-spacing: -0.01em;
        }}

        .ref-search {{
            min-width: 280px;
            height: 32px;
            padding: 0 12px;
            background: {REFERENCE_COLORS['secondary']};
            border: 1px solid {REFERENCE_COLORS['border']};
            border-radius: {REFERENCE_RADIUS['lg']};
            font-size: 13px;
            color: {REFERENCE_COLORS['muted_foreground']};
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .ref-topbar-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .ref-icon-btn {{
            width: 32px;
            height: 32px;
            border-radius: {REFERENCE_RADIUS['md']};
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            transition: background 150ms;
        }}

        .ref-icon-btn:hover {{
            background: {REFERENCE_COLORS['secondary']};
        }}

        .ref-avatar {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: oklch(0.6 0.2 256);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 600;
        }}
        </style>

        <div class="ref-topbar">
            <div class="ref-topbar-left">
                <div class="ref-logo">🎓</div>
                <div class="ref-app-title">{app_title}</div>
                <div class="ref-search">
                    <span style="opacity: 0.5;">🔍</span>
                    <span>Search...</span>
                    <span style="margin-left: auto; opacity: 0.4; font-size: 11px;">⌘K</span>
                </div>
            </div>
            <div class="ref-topbar-right">
                <div class="ref-icon-btn">🔔</div>
                <div class="ref-avatar">{initials}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar(active_page: str, on_page_change: Callable[[str], None]):
    """
    Render Sidebar exactly matching reference AppShell.tsx
    Width: 220px, Sections: Main, Insights, System, Demo
    """

    # Sidebar navigation structure from reference
    sections = {
        "Main": [
            ("Dashboard", "📊"),
            ("Attendance", "✓"),
            ("Students", "👥"),
            ("Classes", "📚"),
        ],
        "Insights": [
            ("Analytics", "📈"),
            ("Reports", "📄"),
        ],
        "System": [
            ("Settings", "⚙️"),
            ("Help", "❓"),
        ],
        "Demo": [
            ("Student Portal", "🎓"),
        ],
    }

    st.markdown(f"""
        <style>
        .ref-sidebar {{
            width: 220px;
            height: calc(100vh - 56px);
            position: fixed;
            left: 0;
            top: 56px;
            background: {REFERENCE_COLORS['sidebar_bg']};
            backdrop-filter: blur(20px);
            border-right: 1px solid {REFERENCE_COLORS['border']};
            padding: 16px 12px;
            overflow-y: auto;
        }}

        .ref-sidebar-section {{
            margin-bottom: 20px;
        }}

        .ref-sidebar-label {{
            font-size: 11px;
            font-weight: 600;
            color: {REFERENCE_COLORS['muted_foreground']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0 8px 6px 8px;
        }}

        .ref-sidebar-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 7px 10px;
            border-radius: {REFERENCE_RADIUS['md']};
            font-size: 13.5px;
            color: {REFERENCE_COLORS['muted_foreground']};
            cursor: pointer;
            transition: all 150ms;
            text-decoration: none;
            margin-bottom: 2px;
        }}

        .ref-sidebar-item:hover {{
            background: {REFERENCE_COLORS['accent']};
            color: {REFERENCE_COLORS['primary']};
        }}

        .ref-sidebar-item.active {{
            background: {REFERENCE_COLORS['accent']};
            color: {REFERENCE_COLORS['accent_foreground']};
            font-weight: 500;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Render sidebar
    sidebar_html = '<div class="ref-sidebar">'

    for section_name, items in sections.items():
        sidebar_html += f'<div class="ref-sidebar-section">'
        sidebar_html += f'<div class="ref-sidebar-label">{section_name}</div>'

        for page_name, icon in items:
            active_class = "active" if active_page == page_name else ""
            sidebar_html += f'<div class="ref-sidebar-item {active_class}" onclick="window.parent.postMessage({{type: \'streamlit:setComponentValue\', key: \'nav\', value: \'{page_name}\'}}, \'*\')">'
            sidebar_html += f'<span>{icon}</span><span>{page_name}</span>'
            sidebar_html += '</div>'

        sidebar_html += '</div>'

    sidebar_html += '</div>'

    st.markdown(sidebar_html, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, date_pill: Optional[str] = None):
    """
    Render PageHeader exactly matching reference ui.tsx
    """

    st.markdown(f"""
        <style>
        .ref-page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 24px;
        }}

        .ref-page-header-left h1 {{
            font-size: 28px !important;
            font-weight: 600 !important;
            color: {REFERENCE_COLORS['primary']} !important;
            margin: 0 !important;
            line-height: 1.2 !important;
        }}

        .ref-page-header-left p {{
            font-size: 14px !important;
            color: {REFERENCE_COLORS['muted_foreground']} !important;
            margin: 4px 0 0 0 !important;
        }}

        .ref-date-pill {{
            padding: 4px 12px;
            background: {REFERENCE_COLORS['card']};
            border: 1px solid {REFERENCE_COLORS['border']};
            border-radius: {REFERENCE_RADIUS['xl']};
            font-size: 12px;
            color: {REFERENCE_COLORS['muted_foreground']};
            box-shadow: {REFERENCE_SHADOWS['control']};
        }}
        </style>

        <div class="ref-page-header">
            <div class="ref-page-header-left">
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            {f'<div class="ref-date-pill">{date_pill}</div>' if date_pill else ''}
        </div>
    """, unsafe_allow_html=True)


def render_stat_card(icon: str, label: str, value: str, hint: str, trend: Optional[Literal["up", "down"]] = None):
    """
    Render StatCard exactly matching reference ui.tsx
    """

    trend_html = ""
    if trend == "up":
        trend_html = '<span style="color: oklch(0.66 0.17 150); font-size: 12px;">↑</span>'
    elif trend == "down":
        trend_html = '<span style="color: oklch(0.64 0.22 27); font-size: 12px;">↓</span>'

    st.markdown(f"""
        <style>
        .ref-stat-card {{
            background: {REFERENCE_COLORS['card']};
            border: 1px solid {REFERENCE_COLORS['border']};
            border-radius: {REFERENCE_RADIUS['3xl']};
            padding: 20px;
            box-shadow: {REFERENCE_SHADOWS['panel']};
            transition: box-shadow 200ms, transform 200ms;
        }}

        .ref-stat-card:hover {{
            box-shadow: {REFERENCE_SHADOWS['panel_hover']};
            transform: translateY(-1px);
        }}

        .ref-stat-label {{
            font-size: 12.5px;
            color: {REFERENCE_COLORS['muted_foreground']};
            font-weight: 500;
            margin-bottom: 12px;
        }}

        .ref-stat-value {{
            font-size: 28px;
            font-weight: 600;
            color: {REFERENCE_COLORS['primary']};
            line-height: 1;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .ref-stat-hint {{
            font-size: 12px;
            color: {REFERENCE_COLORS['muted_foreground']};
        }}
        </style>

        <div class="ref-stat-card">
            <div class="ref-stat-label">{icon} {label}</div>
            <div class="ref-stat-value">{value} {trend_html}</div>
            <div class="ref-stat-hint">{hint}</div>
        </div>
    """, unsafe_allow_html=True)


def render_panel(title: Optional[str] = None, subtitle: Optional[str] = None, hover: bool = False):
    """
    Render Panel exactly matching reference ui.tsx
    Returns a container that children can be placed into
    """

    hover_class = "ref-panel-hover" if hover else ""

    st.markdown(f"""
        <style>
        .ref-panel {{
            background: {REFERENCE_COLORS['card']};
            border: 1px solid {REFERENCE_COLORS['border']};
            border-radius: {REFERENCE_RADIUS['3xl']};
            padding: 24px;
            box-shadow: {REFERENCE_SHADOWS['panel']};
        }}

        .ref-panel-hover {{
            transition: box-shadow 200ms, transform 200ms;
        }}

        .ref-panel-hover:hover {{
            box-shadow: {REFERENCE_SHADOWS['panel_hover']};
            transform: translateY(-1px);
        }}

        .ref-panel-title {{
            font-size: 15px;
            font-weight: 600;
            color: {REFERENCE_COLORS['primary']};
            margin-bottom: 4px;
        }}

        .ref-panel-subtitle {{
            font-size: 12.5px;
            color: {REFERENCE_COLORS['muted_foreground']};
            margin-bottom: 16px;
        }}
        </style>
    """, unsafe_allow_html=True)

    panel_start = f'<div class="ref-panel {hover_class}">'
    if title:
        panel_start += f'<div class="ref-panel-title">{title}</div>'
    if subtitle:
        panel_start += f'<div class="ref-panel-subtitle">{subtitle}</div>'

    return panel_start  # Caller must close with </div>


def render_status_badge(status: Literal["present", "absent", "late"]):
    """
    Render StatusBadge exactly matching reference ui.tsx
    """

    status_config = {
        "present": ("Present", "oklch(0.66 0.17 150)", "oklch(0.66 0.17 150 / 0.15)"),
        "absent": ("Absent", "oklch(0.64 0.22 27)", "oklch(0.64 0.22 27 / 0.12)"),
        "late": ("Late", "oklch(0.72 0.17 60)", "oklch(0.72 0.17 60 / 0.15)"),
    }

    label, text_color, bg_color = status_config[status]

    return f'''
        <span style="
            display: inline-flex;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
            color: {text_color};
            background: {bg_color};
        ">{label}</span>
    '''


def render_avatar(name: str, size: int = 32):
    """
    Render Avatar with initials exactly matching reference ui.tsx
    """

    initials = ''.join([part[0] for part in name.split()][:2]).upper()

    return f'''
        <div style="
            width: {size}px;
            height: {size}px;
            border-radius: 50%;
            background: oklch(0.6 0.2 256);
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: {size * 0.4}px;
            font-weight: 600;
        ">{initials}</div>
    '''


def render_main_content_area():
    """
    Render main content area with proper offset for TopBar and Sidebar
    """

    st.markdown("""
        <style>
        .ref-main {{
            margin-left: 220px;
            margin-top: 56px;
            padding: 32px;
            min-height: calc(100vh - 56px);
        }}
        </style>

        <div class="ref-main">
    """, unsafe_allow_html=True)
