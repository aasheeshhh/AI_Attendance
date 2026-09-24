import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout,style_background_home
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

    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.header("Continue as Teacher")
            st.image(str(Teacher), width=145)

            if st.button("Teacher Portal", type="primary"):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.header("Continue as Student")
            st.image(str(Student), width=145)

            if st.button("Student Portal", type="primary"):
                st.session_state["login_type"] = "student"
                st.rerun()