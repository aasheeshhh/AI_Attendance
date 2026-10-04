"""
Teacher Screen - Reference-Inspired macOS Style
Complete teacher dashboard with attendance, subjects, and records
Matching the visual design of pixel-perfect-snap-8916
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
    """Teacher dashboard with reference-inspired layout and navigation"""

    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data['teacher_id']

    # Get subjects and records for stats
    subjects = get_teacher_subjects(teacher_id)
    records = get_attendance_for_teacher(teacher_id)

    # Calculate overview stats
    total_subjects = len(subjects) if subjects else 0
    total_students = sum(s.get('total_students', 0) for s in subjects) if subjects else 0
    total_sessions = len(set(r.get('timestamp') for r in records)) if records else 0

    # Top bar inspired by reference
    st.markdown(f"""
        <style>
        .top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: {SPACING['md']} 0;
            margin-bottom: {SPACING['lg']};
            border-bottom: 1px solid {COLORS['border']};
        }}

        .top-bar-left {{
            display: flex;
            align-items: center;
            gap: {SPACING['md']};
        }}

        .top-bar-right {{
            display: flex;
            align-items: center;
            gap: {SPACING['md']};
        }}

        .user-badge {{
            display: flex;
            align-items: center;
            gap: {SPACING['sm']};
            background: {COLORS['surface_primary']};
            padding: {SPACING['xs']} {SPACING['md']};
            border-radius: {RADIUS['xl']};
            border: 1px solid {COLORS['border']};
            box-shadow: {SHADOWS['control']};
        }}

        .user-avatar {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: {COLORS['blue']};
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .user-info {{
            text-align: left;
        }}

        .user-name {{
            font-size: 0.8125rem !important;
            font-weight: 600 !important;
            color: {COLORS['text_primary']} !important;
            line-height: 1.2 !important;
        }}

        .user-role {{
            font-size: 0.6875rem !important;
            color: {COLORS['text_tertiary']} !important;
            line-height: 1 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Top Bar
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()

    with c2:
        cols = st.columns([2, 1], vertical_alignment='center')
        with cols[0]:
            initials = ''.join([part[0] for part in teacher_data['name'].split()][:2]).upper()
            st.markdown(f"""
                <div class="user-badge">
                    <div class="user-avatar">{initials}</div>
                    <div class="user-info">
                        <div class="user-name">{teacher_data['name']}</div>
                        <div class="user-role">Teacher</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with cols[1]:
            if st.button("Sign Out", type='secondary', key='teacher_logout', icon=':material/logout:', width='stretch'):
                st.session_state['is_logged_in'] = False
                del st.session_state.teacher_data
                st.rerun()

    # Page Header (Reference Style)
    date_str = datetime.now().strftime("%A, %B %d")
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: {SPACING['xl']};">
            <div>
                <h1 style="margin: 0; font-size: 1.75rem;">Teacher Dashboard</h1>
                <p style="margin: {SPACING['xs']} 0 0 0; color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                    Manage attendance, subjects, and view class insights
                </p>
            </div>
            <div style="background: {COLORS['surface_primary']}; padding: 4px 12px; border-radius: {RADIUS['xl']}; font-size: 0.75rem; color: {COLORS['text_secondary']}; border: 1px solid {COLORS['border']}; box-shadow: {SHADOWS['control']};">
                📅 {date_str}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Stat Cards Row (Reference Style)
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Total Classes</div>
                <div class="stat-card-value">{total_subjects}</div>
                <div class="stat-card-hint">Active subjects</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Total Students</div>
                <div class="stat-card-value">{total_students}</div>
                <div class="stat-card-hint">Enrolled across classes</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Attendance Sessions</div>
                <div class="stat-card-value">{total_sessions}</div>
                <div class="stat-card-hint">Total recorded</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">AI Status</div>
                <div class="stat-card-value" style="color: {COLORS['success']};">Ready</div>
                <div class="stat-card-hint">Face & Voice recognition</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<div style='height: {SPACING['xl']};'></div>", unsafe_allow_html=True)

    # Navigation Section Tabs (Reference Style)
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
        if st.button('Manage Classes', type=type2, width='stretch', icon=':material/school:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "secondary"
        if st.button('Attendance Records', type=type3, width='stretch', icon=':material/analytics:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

    # Route to appropriate tab
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    """Take attendance tab with reference-inspired panel layout"""

    teacher_id = st.session_state.teacher_data['teacher_id']

    st.markdown(f"""
        <div class="panel" style="margin-bottom: {SPACING['xl']};">
            <h2 style="margin: 0 0 {SPACING['xs']} 0;">Take Attendance</h2>
            <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.875rem;">
                Select a class and choose your preferred AI recognition method
            </p>
        </div>
    """, unsafe_allow_html=True)

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('📚 You haven\'t created any classes yet. Create one in "Manage Classes" to begin taking attendance.')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Class', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/add_a_photo:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

    # Display added photos in panel
    if st.session_state.attendance_images:
        st.markdown(f"""
            <div class="panel" style="margin-bottom: {SPACING['lg']};">
                <h3 style="margin: 0 0 {SPACING['md']} 0;">Classroom Photos ({len(st.session_state.attendance_images)})</h3>
        """, unsafe_allow_html=True)

        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')

        st.markdown("</div>", unsafe_allow_html=True)

    has_photos = bool(st.session_state.attendance_images)

    # Action buttons
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear Photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
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
        if st.button('Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    """Manage subjects tab with reference-inspired card grid"""

    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns([3, 1], vertical_alignment='center')

    with col1:
        st.markdown(f"""
            <div>
                <h2 style="margin: 0;">Manage Classes</h2>
                <p style="color: {COLORS['text_secondary']}; margin: {SPACING['xs']} 0 0 0; font-size: 0.875rem;">
                    Create and manage your course roster
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button('Create Class', width='stretch', type='primary', icon=':material/add:'):
            create_subject_dialog(teacher_id)

    st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

    # List all subjects in grid
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        cols = st.columns(2)
        for i, sub in enumerate(subjects):
            stats = [
                ("👥", "Students", sub['total_students']),
                ("📅", "Sessions", sub['total_classes']),
            ]

            def share_btn(subject=sub):
                if st.button(f"Share Code", key=f"share_{subject['subject_code']}", icon=":material/share:", width='stretch'):
                    share_subject_dialog(subject['name'], subject['subject_code'])

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=stats,
                    footer_callback=share_btn
                )
    else:
        st.info("📚 No classes found. Create one above to get started.")


def teacher_tab_attendance_records():
    """Attendance records tab with reference table styling"""

    st.markdown(f"""
        <div class="panel" style="margin-bottom: {SPACING['xl']};">
            <h2 style="margin: 0 0 {SPACING['xs']} 0;">Attendance Records</h2>
            <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.875rem;">
                Historical attendance sessions across all your classes
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
            "Date & Time": datetime.fromisoformat(ts).strftime("%b %d, %Y • %I:%M %p") if ts else "N/A",
            "Class Name": r['subjects']['name'],
            "Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Date & Time', 'Class Name', 'Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Rate'] = (
        (summary['Present_Count'] / summary['Total_Count'] * 100).round(1).astype(str) + "%"
    )

    summary['Status'] = (
        summary['Present_Count'].astype(str) + "/" +
        summary['Total_Count'].astype(str) + ' present'
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Date & Time', 'Class Name', 'Code', 'Attendance Rate', 'Status']]
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
    """Teacher login screen with reference panel style"""

    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Login form in centered panel
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div class="panel" style="text-align: center; margin-bottom: {SPACING['lg']};">
                <h2 style="margin: 0 0 {SPACING['xs']} 0;">Teacher Login</h2>
                <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.875rem;">
                    Sign in to access your dashboard
                </p>
            </div>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='Enter your username', label_visibility='collapsed')
        teacher_pass = st.text_input("Password", type='password', placeholder="Enter your password", label_visibility='collapsed')

        st.markdown(f"<div style='height: {SPACING['md']};'></div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Login', icon=':material/login:', width='stretch', type='primary'):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("👋 Welcome back!", icon="✅")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with btnc2:
            if st.button('Create Account', type="secondary", width='stretch'):
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
    """Teacher registration screen with reference panel style"""

    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Back to Home", type='secondary', key='registerbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Registration form in centered panel
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div class="panel" style="text-align: center; margin-bottom: {SPACING['lg']};">
                <h2 style="margin: 0 0 {SPACING['xs']} 0;">Create Teacher Account</h2>
                <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.875rem;">
                    Register to start taking AI attendance
                </p>
            </div>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='Choose a username', label_visibility='collapsed')
        teacher_name = st.text_input("Full Name", placeholder='Enter your full name', label_visibility='collapsed')
        teacher_pass = st.text_input("Password", type='password', placeholder="Create a password", label_visibility='collapsed')
        teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="Confirm your password", label_visibility='collapsed')

        st.markdown(f"<div style='height: {SPACING['md']};'></div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Register', icon=':material/person_add:', width='stretch', type='primary'):
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
