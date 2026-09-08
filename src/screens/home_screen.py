import streamlit as st

from src.components.header import header_home
from src.ui.base_layout import style_base_layout


def home_screen():

    # Apply global styling
    style_base_layout()

    # Header / Hero
    header_home()

    # Small subtitle
    st.markdown(
        """
        <div class="home-subtitle">
            Choose how you want to continue
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Portal buttons
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        if st.button(
            "Teacher Portal",
            width="stretch",
            key="teacher_portal"
        ):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    with col2:
        if st.button(
            "Student Portal",
            width="stretch",
            key="student_portal"
        ):
            st.session_state["login_type"] = "student"
            st.rerun()

    # Footer
    st.markdown(
        """
        <div class="home-footer">
            Secure&nbsp;&nbsp;•&nbsp;&nbsp;Simple&nbsp;&nbsp;•&nbsp;&nbsp;Connected
        </div>
        """,
        unsafe_allow_html=True,
    )
