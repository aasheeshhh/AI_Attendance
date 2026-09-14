import streamlit as st

from src.components.header import show_header
from src.ui.base_layout import apply_home_style


def show_portal(title: str, description: str, button_text: str, user_type: str):
    """Show one portal card and save the selected user type."""
    st.markdown(
        f"""
        <div class="portal-copy">
            <p class="portal-label">{title}</p>
            <p class="portal-description">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(button_text, width="stretch", key=f"{user_type}_portal"):
        st.session_state["login_type"] = user_type
        st.rerun()


def show_home():
    apply_home_style()
    show_header()

    st.markdown(
        """
        <section class="home-hero">
            <p class="home-eyebrow">Welcome</p>
            <h1 class="home-title">Choose how you want to continue</h1>
            <p class="home-subtitle">
                A simpler way to stay present, connected, and on track.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="portal-container-anchor"></div>', unsafe_allow_html=True)
        teacher_column, student_column = st.columns(2, gap="large")

        with teacher_column:
            show_portal(
                "Teacher Portal",
                "Manage classes and keep attendance in view.",
                "Continue as Teacher →",
                "teacher",
            )

        with student_column:
            show_portal(
                "Student Portal",
                "View your attendance and class information.",
                "Continue as Student →",
                "student",
            )

    st.markdown(
        '<div class="home-footer">Secure&nbsp;&nbsp;•&nbsp;&nbsp;Simple&nbsp;&nbsp;•&nbsp;&nbsp;Connected</div>',
        unsafe_allow_html=True,
    )
