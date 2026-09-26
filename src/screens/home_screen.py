import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.ui.portal_cards import style_portal_cards
from pathlib import Path


def home_screen():

    Student = (
        Path(__file__).resolve().parent.parent.parent
        / "assets"
        / "Student.png"
    )

    Teacher = (
        Path(__file__).resolve().parent.parent.parent
        / "assets"
        / "Teacher.png"
    )

    header_home()
    style_background_home()
    style_base_layout()
    style_portal_cards()

    with st.container(key="portal_section"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            with st.container(key="teacher_card"):
                st.markdown('<div class="portal-title">Continue as Teacher</div>', unsafe_allow_html=True)

                with st.container(key="teacher_image"):
                    st.image(str(Teacher), width=280)

                with st.container(key="teacher_button"):
                    if st.button("Teacher Portal", type="primary", use_container_width=True):
                        st.session_state["login_type"] = "teacher"
                        st.rerun()

        with col2:
            with st.container(key="student_card"):
                st.markdown('<div class="portal-title">Continue as Student</div>', unsafe_allow_html=True)

                with st.container(key="student_image"):
                    st.image(str(Student), width=280)

                with st.container(key="student_button"):
                    if st.button("Student Portal", type="primary", use_container_width=True):
                        st.session_state["login_type"] = "student"
                        st.rerun()