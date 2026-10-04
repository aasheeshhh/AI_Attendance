"""
Home / Landing Screen - Reference-Inspired macOS Style
Clean portal selection with refined panel design
"""

import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.ui.macos_design_system import COLORS, SPACING, RADIUS, SHADOWS


def home_screen():
    """Main landing screen for role selection with reference design"""

    style_background_home()
    style_base_layout()

    header_home()

    # Custom styling for portal cards (reference panel style)
    st.markdown(f"""
        <style>
        .portal-card {{
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['xxl']};
            padding: {SPACING['xxl']};
            text-align: center;
            transition: all 200ms ease;
            box-shadow: {SHADOWS['panel']};
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 320px;
        }}

        .portal-card:hover {{
            transform: translateY(-2px);
            box-shadow: {SHADOWS['panel_hover']};
        }}

        .portal-icon {{
            margin-bottom: {SPACING['lg']};
            transition: transform 200ms ease;
        }}

        .portal-card:hover .portal-icon {{
            transform: scale(1.05);
        }}

        .portal-title {{
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            margin-bottom: {SPACING['sm']} !important;
            letter-spacing: -0.02em !important;
        }}

        .portal-desc {{
            font-size: 0.9375rem !important;
            color: {COLORS['text_secondary']} !important;
            margin-bottom: {SPACING['xl']} !important;
            line-height: 1.5 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
            <div class="portal-card">
                <div>
                    <div class="portal-icon">
                        <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="140" style="border-radius: {RADIUS['xl']};" />
                    </div>
                    <div class="portal-title">Teacher</div>
                    <div class="portal-desc">Manage classes and take AI-powered attendance with face and voice recognition</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Continue as Teacher', type='primary', icon=':material/arrow_forward:', use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with col2:
        st.markdown(f"""
            <div class="portal-card">
                <div>
                    <div class="portal-icon">
                        <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" width="120" style="border-radius: {RADIUS['xl']};" />
                    </div>
                    <div class="portal-title">Student</div>
                    <div class="portal-desc">Check in with Face ID and view your attendance history across all classes</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Continue as Student', type='primary', icon=':material/arrow_forward:', use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()

    footer_home()
