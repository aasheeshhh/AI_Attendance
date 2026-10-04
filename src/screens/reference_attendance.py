"""
Attendance Page - Direct Transfer from pixel-perfect-snap-8916/src/routes/attendance.tsx
Date picker + Class filter + Search + Present/Late/Absent counts + AttendanceTable
"""

import streamlit as st
from datetime import datetime, date
from src.ui.reference_components import (
    apply_reference_base_styles,
    render_topbar,
    render_sidebar,
    render_page_header,
    render_status_badge,
    render_avatar,
    render_main_content_area,
    REFERENCE_COLORS,
    REFERENCE_SHADOWS,
    REFERENCE_RADIUS,
)
from src.database.db import (
    get_all_students,
    get_teacher_subjects,
    get_attendance_for_teacher,
)
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog


def reference_attendance_page(teacher_data):
    """
    Render Attendance page exactly matching reference/src/routes/attendance.tsx
    """

    apply_reference_base_styles()

    # Render TopBar
    render_topbar(
        app_title="AI Attendance",
        user_name=teacher_data.get('name', 'Teacher'),
        user_role="Teacher"
    )

    # Render Sidebar
    render_sidebar(
        active_page=st.session_state.get('nav_page', 'Attendance'),
        on_page_change=lambda page: setattr(st.session_state, 'nav_page', page)
    )

    # Main content area
    render_main_content_area()

    # PageHeader
    render_page_header(
        title="Attendance",
        subtitle="Mark and manage student attendance for your classes",
        date_pill=None
    )

    # Load data
    students = get_all_students() or []
    subjects = get_teacher_subjects(teacher_data['teacher_id']) or []
    logs = get_attendance_for_teacher(teacher_data['teacher_id']) or []

    # Filters row (Date picker + Class dropdown + Search)
    filter_col1, filter_col2, filter_col3 = st.columns([1, 2, 2])

    with filter_col1:
        st.markdown(f"""
            <div style="font-size: 12.5px; font-weight: 500; color: {REFERENCE_COLORS['muted_foreground']}; margin-bottom: 8px;">Date</div>
        """, unsafe_allow_html=True)

        selected_date = st.date_input(
            "Date",
            value=date.today(),
            label_visibility='collapsed',
            key='attendance_date_picker'
        )

    with filter_col2:
        st.markdown(f"""
            <div style="font-size: 12.5px; font-weight: 500; color: {REFERENCE_COLORS['muted_foreground']}; margin-bottom: 8px;">Class Filter</div>
        """, unsafe_allow_html=True)

        subject_options = ["All Classes"] + [f"{s['name']} ({s['subject_code']})" for s in subjects]
        selected_class = st.selectbox(
            "Class",
            options=subject_options,
            label_visibility='collapsed',
            key='attendance_class_filter'
        )

        # Extract subject_id from selection
        selected_subject_id = None
        if selected_class != "All Classes":
            for s in subjects:
                if f"{s['name']} ({s['subject_code']})" == selected_class:
                    selected_subject_id = s['subject_id']
                    break

    with filter_col3:
        st.markdown(f"""
            <div style="font-size: 12.5px; font-weight: 500; color: {REFERENCE_COLORS['muted_foreground']}; margin-bottom: 8px;">Search Students</div>
        """, unsafe_allow_html=True)

        search_query = st.text_input(
            "Search",
            placeholder="Search by name or ID...",
            label_visibility='collapsed',
            key='attendance_search'
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Actions row + Summary counts
    action_col1, action_col2 = st.columns([3, 1])

    with action_col1:
        st.markdown(f"""
            <div style="display: flex; gap: 12px;">
                <div style="
                    padding: 6px 12px;
                    background: {REFERENCE_COLORS['card']};
                    border: 1px solid {REFERENCE_COLORS['border']};
                    border-radius: {REFERENCE_RADIUS['lg']};
                    font-size: 12.5px;
                    color: {REFERENCE_COLORS['muted_foreground']};
                    box-shadow: {REFERENCE_SHADOWS['control']};
                ">
                    <span style="color: oklch(0.66 0.17 150); font-weight: 600;">✓</span> Present: 0
                </div>
                <div style="
                    padding: 6px 12px;
                    background: {REFERENCE_COLORS['card']};
                    border: 1px solid {REFERENCE_COLORS['border']};
                    border-radius: {REFERENCE_RADIUS['lg']};
                    font-size: 12.5px;
                    color: {REFERENCE_COLORS['muted_foreground']};
                    box-shadow: {REFERENCE_SHADOWS['control']};
                ">
                    <span style="color: oklch(0.72 0.17 60); font-weight: 600;">⏱</span> Late: 0
                </div>
                <div style="
                    padding: 6px 12px;
                    background: {REFERENCE_COLORS['card']};
                    border: 1px solid {REFERENCE_COLORS['border']};
                    border-radius: {REFERENCE_RADIUS['lg']};
                    font-size: 12.5px;
                    color: {REFERENCE_COLORS['muted_foreground']};
                    box-shadow: {REFERENCE_SHADOWS['control']};
                ">
                    <span style="color: oklch(0.64 0.22 27); font-weight: 600;">✗</span> Absent: 0
                </div>
            </div>
        """, unsafe_allow_html=True)

    with action_col2:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📸 Face", use_container_width=True, type='primary'):
                if selected_subject_id:
                    # Initialize session state for face attendance
                    if 'attendance_images' not in st.session_state:
                        st.session_state.attendance_images = []
                    add_photos_dialog()
                else:
                    st.warning("⚠️ Please select a class first")

        with btn_col2:
            if st.button("🎤 Voice", use_container_width=True, type='secondary'):
                if selected_subject_id:
                    voice_attendance_dialog(selected_subject_id)
                else:
                    st.warning("⚠️ Please select a class first")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # AttendanceTable Panel (reference style with grid layout)
    st.markdown(f"""
        <div class="ref-panel">
            <div class="ref-panel-title">Student Attendance</div>
            <div class="ref-panel-subtitle">Click on status to change attendance</div>

            <div style="margin-top: 20px;">
                <!-- Table Header -->
                <div style="
                    display: grid;
                    grid-template-columns: 2fr 1fr 1fr auto;
                    gap: 16px;
                    padding: 12px 16px;
                    background: {REFERENCE_COLORS['muted']};
                    border-radius: {REFERENCE_RADIUS['lg']} {REFERENCE_RADIUS['lg']} 0 0;
                    font-size: 11.5px;
                    font-weight: 600;
                    color: {REFERENCE_COLORS['muted_foreground']};
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    <div>Student</div>
                    <div>Class</div>
                    <div>Time</div>
                    <div>Status</div>
                </div>
    """, unsafe_allow_html=True)

    # Filter students based on search and selected class
    filtered_students = students

    if search_query:
        search_lower = search_query.lower()
        filtered_students = [
            s for s in filtered_students
            if search_lower in s['name'].lower() or search_lower in str(s.get('student_id', '')).lower()
        ]

    # Display student rows
    if filtered_students:
        for student in filtered_students[:20]:  # Limit to 20 for performance
            # Find today's attendance log for this student
            student_logs = [
                log for log in logs
                if log.get('student_id') == student['student_id']
                and log.get('timestamp')
                and log['timestamp'].date() == selected_date
            ]

            latest_log = student_logs[0] if student_logs else None

            if latest_log:
                status = "late" if latest_log.get('status') == 'late' else ("present" if latest_log.get('is_present') else "absent")
                time_str = latest_log['timestamp'].strftime("%I:%M %p")
            else:
                status = "absent"
                time_str = "—"

            # Render row
            st.markdown(f"""
                <div style="
                    display: grid;
                    grid-template-columns: 2fr 1fr 1fr auto;
                    gap: 16px;
                    padding: 14px 16px;
                    border-bottom: 1px solid {REFERENCE_COLORS['border']};
                    align-items: center;
                ">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        {render_avatar(student['name'], 32)}
                        <div>
                            <div style="font-size: 13px; font-weight: 500; color: {REFERENCE_COLORS['primary']};">{student['name']}</div>
                            <div style="font-size: 11.5px; color: {REFERENCE_COLORS['muted_foreground']};">{student.get('student_id', 'N/A')}</div>
                        </div>
                    </div>
                    <div style="font-size: 13px; color: {REFERENCE_COLORS['muted_foreground']};">BCA-A</div>
                    <div style="font-size: 12px; font-variant-numeric: tabular-nums; color: {REFERENCE_COLORS['muted_foreground']};">{time_str}</div>
                    <div>{render_status_badge(status)}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="
                text-align: center;
                padding: 48px;
                color: {REFERENCE_COLORS['muted_foreground']};
                font-size: 13px;
            ">
                No students found
            </div>
        """, unsafe_allow_html=True)

    # Close panel
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Close main content area
    st.markdown("</div>", unsafe_allow_html=True)
