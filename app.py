"""
Main Application Entry Point - macOS Style
"""

import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.ui.macos_design_system import apply_macos_base_styles


def main():
    """Main application entry point"""

    st.set_page_config(
        page_title='SnapClass — AI Attendance',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Apply global macOS styles
    apply_macos_base_styles()

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # Route based on login type
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            home_screen()

    # Handle join code in query params
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)


if __name__ == "__main__":
    main()
