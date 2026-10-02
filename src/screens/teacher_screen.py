"""
Teacher Screen - macOS Style
Complete teacher dashboard with attendance, subjects, and records
Preserving all existing functionality with new macOS visual design
"""

import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.ui.macos_design_system import COLORS, SPACING, RADIUS, SHADOWS
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists, create_teacher, teacher_login,
    get_teacher_subjects, get_attendance_for_teacher
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.config import require_supabase

import numpy as np
from datetime import datetime
import pandas as pd


def teacher_screen():
    """Main teacher screen router"""

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    """Teacher dashboard with tabs for attendance, subjects, and records"""

    teacher_data = st.session_state.teacher_data

    # macOS-style navigation tabs
    st.markdown(f"""
        <style>
        .teacher-nav {{
            display: flex;
            gap: {SPACING['sm']};
            padding: {SPACING['md']} 0;
            border-bottom: 1px solid {COLORS['border']};
            margin-bottom: {SPACING['xl']};
        }}

        .teacher-nav-item {{
            padding: {SPACING['sm']} {SPACING['lg']};
            border-radius: {RADIUS['md']};
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: {COLORS['text_secondary']} !important;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .teacher-nav-item.active {{
            background: {COLORS['blue']};
            color: white !important;
        }}

        .teacher-nav-item:hover:not(.active) {{
            background: {COLORS['surface_secondary']};
        }}

        .welcome-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: {SPACING['lg']};
            background: {COLORS['surface_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: {RADIUS['lg']};
            margin-bottom: {SPACING['xl']};
        }}

        .welcome-text {{
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            margin: 0 !important;
        }}

        .welcome-subtitle {{
            font-size: 0.875rem !important;
            color: {COLORS['text_secondary']} !important;
            margin-top: {SPACING['xs']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Welcome section with logout
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()

    with c2:
        st.markdown(f"""
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: {COLORS['text_tertiary']};">Logged in as</div>
                <div style="font-size: 0.9375rem; font-weight: 600; color: {COLORS['text_primary']};">{teacher_data['name']}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", type='secondary', key='teacher_logout', shortcut="control+backspace", icon=':material/logout:'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation tabs
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "secondary"
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/how_to_reg:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "secondary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/school:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "secondary"
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/analytics:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    # Route to appropriate tab
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    """Take attendance tab - face or voice recognition"""

    teacher_id = st.session_state.teacher_data['teacher_id']

    st.markdown(f"""
        <div style="margin-bottom: {SPACING['lg']};">
            <h2 style="margin-bottom: {SPACING['xs']};">Take Attendance</h2>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.9375rem;">
                Use AI-powered face or voice recognition to mark attendance
            </p>
        </div>
    """, unsafe_allow_html=True)

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('📚 You haven\'t created any subjects yet. Create one to begin taking attendance.')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/add_a_photo:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # Display added photos
    if st.session_state.attendance_images:
        st.markdown(f"<h3 style='margin-bottom: {SPACING['md']};'>Added Photos ({len(st.session_state.attendance_images)})</h3>", unsafe_allow_html=True)
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)

    # Action buttons
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear All Photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.session_state.pop('attendance_image_hashes', None)
            st.session_state.pop('dialog_cam', None)
            st.session_state.pop('dialog_upload', None)
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/face_retouching_natural:', disabled=not has_photos):
            with st.spinner('🔍 Analyzing faces in classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = require_supabase().table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                    return

                results, attendance_to_log = [], []
                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                for node in enrolled_students:
                    student = node['students']
                    sources = all_detected_ids.get(int(student['student_id']), [])
                    is_present = len(sources) > 0

                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Source": ", ".join(sources) if is_present else "-",
                        "Status": "✅ Present" if is_present else "❌ Absent"
                    })

                    attendance_to_log.append({
                        'student_id': student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present)
                    })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    """Manage subjects tab"""

    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        st.markdown(f"""
            <div style="margin-bottom: {SPACING['lg']};">
                <h2 style="margin-bottom: {SPACING['xs']};">Manage Subjects</h2>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9375rem;">
                    Create and manage your courses
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button('Create Subject', width='stretch', type='primary', icon=':material/add:'):
            create_subject_dialog(teacher_id)

    # List all subjects
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("📅", "Classes", sub['total_classes']),
            ]

            def share_btn(subject=sub):
                if st.button(f"Share Code", key=f"share_{subject['subject_code']}", icon=":material/share:", width='stretch'):
                    share_subject_dialog(subject['name'], subject['subject_code'])

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("📚 No subjects found. Create one above to get started.")


def teacher_tab_attendance_records():
    """Attendance records tab"""

    st.markdown(f"""
        <div style="margin-bottom: {SPACING['lg']};">
            <h2 style="margin-bottom: {SPACING['xs']};">Attendance Records</h2>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.9375rem;">
                View all attendance sessions across your subjects
            </p>
        </div>
    """, unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("📊 No attendance records yet. Start taking attendance to see data here.")
        return

    data = []

    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / " +
        summary['Total_Count'].astype(str) + ' students'
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject Code', 'Attendance']]
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)


def login_teacher(username, password):
    """Teacher login validation"""

    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    """Teacher login screen"""

    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Login form in centered container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: {SPACING['xl']};">
                <h2>Teacher Login</h2>
                <p style="color: {COLORS['text_secondary']};">Sign in with your credentials</p>
            </div>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='Enter your username', label_visibility='collapsed')
        teacher_pass = st.text_input("Password", type='password', placeholder="Enter your password", label_visibility='collapsed')

        st.markdown(f"<div style='height: {SPACING['md']};'></div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Login', icon=':material/login:', shortcut='control+enter', width='stretch', type='primary'):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("👋 Welcome back!", icon="✅")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with btnc2:
            if st.button('Register', type="secondary", width='stretch'):
                st.session_state.teacher_login_type = 'register'
                st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    """Teacher registration validation"""

    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required"

    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords don't match"

    try:
        if check_teacher_exists(teacher_username):
            return False, "Username already taken"

        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Account created successfully! Please login."

    except Exception as e:
        return False, "An unexpected error occurred"


def teacher_screen_register():
    """Teacher registration screen"""

    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Back to Home", type='secondary', key='registerbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Registration form in centered container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: {SPACING['xl']};">
                <h2>Create Teacher Account</h2>
                <p style="color: {COLORS['text_secondary']};">Register to start managing attendance</p>
            </div>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='Choose a username', label_visibility='collapsed')
        teacher_name = st.text_input("Full Name", placeholder='Enter your full name', label_visibility='collapsed')
        teacher_pass = st.text_input("Password", type='password', placeholder="Create a password", label_visibility='collapsed')
        teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="Confirm your password", label_visibility='collapsed')

        st.markdown(f"<div style='height: {SPACING['md']};'></div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Register', icon=':material/person_add:', shortcut='control+enter', width='stretch', type='primary'):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    import time
                    time.sleep(2)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button('Login Instead', type="secondary", width='stretch'):
                st.session_state.teacher_login_type = 'login'
                st.rerun()

    footer_dashboard()
