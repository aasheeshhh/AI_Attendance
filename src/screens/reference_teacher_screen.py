"""
Teacher Screen Router - Reference Frontend Sync
Routes to different pages based on sidebar navigation state
"""

import streamlit as st
from src.screens.reference_dashboard import reference_dashboard_screen
from src.screens.reference_attendance import reference_attendance_page
from src.screens.reference_students import reference_students_page
from src.screens.reference_classes import reference_classes_page
from src.ui.reference_components import apply_reference_base_styles


def reference_teacher_screen():
    """
    Main teacher screen router matching reference AppShell structure
    """

    if "teacher_data" not in st.session_state:
        st.error("Please log in first")
        return

    teacher_data = st.session_state.teacher_data

    # Initialize navigation state
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Dashboard"

    current_page = st.session_state.nav_page

    # Route to appropriate page
    if current_page == "Dashboard":
        reference_dashboard_screen(teacher_data)
    elif current_page == "Attendance":
        reference_attendance_page(teacher_data)
    elif current_page == "Students":
        reference_students_page(teacher_data)
    elif current_page == "Classes":
        reference_classes_page(teacher_data)
    elif current_page == "Analytics":
        render_analytics_page(teacher_data)
    elif current_page == "Reports":
        render_reports_page(teacher_data)
    elif current_page == "Settings":
        render_settings_page(teacher_data)
    elif current_page == "Student Portal":
        render_student_portal_demo(teacher_data)
    else:
        reference_dashboard_screen(teacher_data)


def render_attendance_page(teacher_data):
    """Placeholder for Attendance page - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("📋 Attendance")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)


def render_students_page(teacher_data):
    """Placeholder for Students page - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("👥 Students")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)


def render_classes_page(teacher_data):
    """Placeholder for Classes page - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("📚 Classes")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)


def render_analytics_page(teacher_data):
    """Placeholder for Analytics page - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("📈 Analytics")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)


def render_reports_page(teacher_data):
    """Placeholder for Reports page - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("📄 Reports")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)


def render_settings_page(teacher_data):
    """Placeholder for Settings page - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("⚙️ Settings")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)


def render_student_portal_demo(teacher_data):
    """Placeholder for Student Portal demo - will implement exact reference next"""
    apply_reference_base_styles()
    st.markdown("<div style='padding: 100px; text-align: center;'>", unsafe_allow_html=True)
    st.title("🎓 Student Portal")
    st.write("Exact reference implementation coming next...")
    st.markdown("</div>", unsafe_allow_html=True)
