import streamlit as st

from src.screens.home_screen import show_home
from src.screens.student_screen import show_student
from src.screens.teacher_screen import show_teacher


def main():
    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    user_type = st.session_state["login_type"]

    if user_type == "teacher":
        show_teacher()
    elif user_type == "student":
        show_student()
    else:
        show_home()


if __name__ == "__main__":
    main()
