"""
Home / Landing Screen - macOS Style
Clean portal selection with Apple design aesthetic
"""

import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.ui.macos_design_system import COLORS, SPACING, RADIUS, SHADOWS


def home_screen():
    """Main landing screen for role selection"""

    style_background_home()
    style_base_layout()

    header_home()

    # Custom styling for portal cards
    st.markdown(f"""
        <style>
        .portal-card {{
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['xl']};
            padding: {SPACING['xl']};
            text-align: center;
            transition: all 0.2s ease;
            box-shadow: {SHADOWS['sm']};
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
        }}

        .portal-card:hover {{
            transform: translateY(-2px);
            box-shadow: {SHADOWS['md']};
            border-color: {COLORS['border_medium']};
        }}

        .portal-title {{
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            margin-bottom: {SPACING['sm']} !important;
        }}

        .portal-desc {{
            font-size: 0.875rem !important;
            color: {COLORS['text_secondary']} !important;
            margin-bottom: {SPACING['lg']} !important;
        }}

        .portal-icon {{
            margin-bottom: {SPACING['md']};
        }}
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
            <div class="portal-card">
                <div>
                    <div class="portal-icon">
                        <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" width="100" style="border-radius: {RADIUS['lg']};" />
                    </div>
                    <div class="portal-title">Student</div>
                    <div class="portal-desc">Check in with FaceID and view attendance history</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Continue as Student', type='primary', icon=':material/arrow_forward:', icon_position='right', width='stretch'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown(f"""
            <div class="portal-card">
                <div>
                    <div class="portal-icon">
                        <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="120" style="border-radius: {RADIUS['lg']};" />
                    </div>
                    <div class="portal-title">Teacher</div>
                    <div class="portal-desc">Manage classes and take AI-powered attendance</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Continue as Teacher', type='primary', icon=':material/arrow_forward:', icon_position='right', width='stretch'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
