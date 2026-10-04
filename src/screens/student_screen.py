"""
Student Screen - Reference-Inspired macOS Style
Student dashboard with FaceID login and subject enrollment
Matching the visual design of pixel-perfect-snap-8916
"""

import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.ui.macos_design_system import COLORS, SPACING, RADIUS, SHADOWS
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialog
from src.database.db import (
    get_all_students, create_student,
    get_student_subjects, get_student_attendance,
    unenroll_student_to_subject
)
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding

from PIL import Image
import numpy as np
import time
from datetime import datetime


def student_screen():
    """Main student screen router"""

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    student_screen_login()


def student_dashboard():
    """Student dashboard with reference-inspired layout and stat cards"""

    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # Load subjects and attendance data
    with st.spinner('Loading your enrolled classes...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # Calculate attendance stats
    total_classes = len(logs)
    attended_classes = sum(1 for log in logs if log.get('is_present'))
    attendance_rate = (attended_classes / total_classes * 100) if total_classes > 0 else 0
    enrolled_count = len(subjects) if subjects else 0

    # Top Bar (Reference Style)
    c1, c2 = st.columns([3, 2], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        cols = st.columns([2, 1], vertical_alignment='center')
        with cols[0]:
            initials = ''.join([part[0] for part in student_data['name'].split()][:2]).upper()
            st.markdown(f"""
                <div class="user-badge" style="display: flex; align-items: center; gap: {SPACING['sm']}; background: {COLORS['surface_primary']}; padding: {SPACING['xs']} {SPACING['md']}; border-radius: {RADIUS['xl']}; border: 1px solid {COLORS['border']}; box-shadow: {SHADOWS['control']};">
                    <div class="user-avatar" style="width: 28px; height: 28px; border-radius: 50%; background: {COLORS['blue']}; color: white; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 600;">{initials}</div>
                    <div class="user-info" style="text-align: left;">
                        <div class="user-name" style="font-size: 0.8125rem; font-weight: 600; color: {COLORS['text_primary']}; line-height: 1.2;">{student_data['name']}</div>
                        <div class="user-role" style="font-size: 0.6875rem; color: {COLORS['text_tertiary']}; line-height: 1;">Student</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with cols[1]:
            if st.button("Sign Out", type='secondary', key='student_logout', icon=':material/logout:', width='stretch'):
                st.session_state['is_logged_in'] = False
                del st.session_state.student_data
                st.rerun()

    # Page Header (Reference Style)
    date_str = datetime.now().strftime("%A, %B %d")
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: {SPACING['xl']};">
            <div>
                <h1 style="margin: 0; font-size: 1.75rem;">Student Portal</h1>
                <p style="margin: {SPACING['xs']} 0 0 0; color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                    Track your attendance and enrolled classes
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
                <div class="stat-card-label">Enrolled Classes</div>
                <div class="stat-card-value">{enrolled_count}</div>
                <div class="stat-card-hint">Active subjects</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Classes Attended</div>
                <div class="stat-card-value">{attended_classes}</div>
                <div class="stat-card-hint">Out of {total_classes} total</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col3:
        rate_color = COLORS['success'] if attendance_rate >= 75 else COLORS['warning'] if attendance_rate >= 60 else COLORS['danger']
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">Attendance Rate</div>
                <div class="stat-card-value" style="color: {rate_color};">{attendance_rate:.1f}%</div>
                <div class="stat-card-hint">{"Good standing" if attendance_rate >= 75 else "Needs attention"}</div>
            </div>
        """, unsafe_allow_html=True)

    with stat_col4:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-card-label">FaceID Status</div>
                <div class="stat-card-value" style="color: {COLORS['success']};">Active</div>
                <div class="stat-card-hint">Biometrics enrolled</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<div style='height: {SPACING['xl']};'></div>", unsafe_allow_html=True)

    # Enrolled Classes Section Header
    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        st.markdown(f"""
            <div>
                <h2 style="margin: 0;">Enrolled Classes</h2>
                <p style="color: {COLORS['text_secondary']}; margin: {SPACING['xs']} 0 0 0; font-size: 0.875rem;">
                    View attendance details for each class
                </p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        if st.button('Enroll in Class', type='primary', width='stretch', icon=':material/add:'):
            enroll_dialog()

    st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

    # Calculate attendance stats per subject
    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    # Display subjects in grid
    if subjects:
        cols = st.columns(2)

        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            # Calculate attendance percentage
            attendance_pct = (stats['attended'] / stats['total'] * 100) if stats['total'] > 0 else 0

            def unenroll_button(student_id=student_id, sid=sid, sub_name=sub['name']):
                if st.button("Unenroll", type='tertiary', width='stretch', icon=':material/remove_circle:', key=f"unenroll_{sid}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f'✅ Unenrolled from {sub_name}')
                    time.sleep(1)
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('📅', 'Sessions', stats['total']),
                        ('✅', 'Attended', stats['attended']),
                        ('📊', 'Rate', f"{attendance_pct:.0f}%"),
                    ],
                    footer_callback=unenroll_button
                )
    else:
        st.info("📚 You're not enrolled in any classes yet. Click 'Enroll in Class' above to join with a code.")

    footer_dashboard()


def student_screen_login():
    """Student login screen with FaceID - Reference panel style"""

    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Back to Home", type='secondary', key='studentbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # FaceID login in centered panel
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div class="panel" style="text-align: center; margin-bottom: {SPACING['lg']};">
                <div style="font-size: 2.5rem; margin-bottom: {SPACING['sm']};">👤</div>
                <h2 style="margin: 0 0 {SPACING['xs']} 0;">Face ID Login</h2>
                <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.875rem;">
                    Look directly into the camera to sign in
                </p>
            </div>
        """, unsafe_allow_html=True)

        show_registration = False
        photo_source = st.camera_input("Position your face in the frame", label_visibility='collapsed')

        if photo_source:
            img = np.array(Image.open(photo_source))

            with st.spinner('🔍 Scanning face...'):
                detected, all_ids, num_faces = predict_attendance(img)

                if num_faces == 0:
                    st.warning('⚠️ No face detected. Please try again.')
                elif num_faces > 1:
                    st.warning('⚠️ Multiple faces detected. Please ensure only one person is in frame.')
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        all_students = get_all_students()
                        student = next((s for s in all_students if s['student_id'] == student_id), None)

                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            st.toast(f'👋 Welcome back, {student["name"]}!')
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info('🆕 Face not recognized. Complete registration below.')
                        show_registration = True

        if show_registration:
            st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div class="ai-surface" style="margin-bottom: {SPACING['md']};">
                    <h3 style="margin: 0 0 {SPACING['xs']} 0;">New Student Registration</h3>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.8125rem; margin: 0;">
                        Your face will be enrolled for automatic attendance
                    </p>
                </div>
            """, unsafe_allow_html=True)

            new_name = st.text_input("Full Name", placeholder='Enter your full name', label_visibility='collapsed')

            st.markdown(f"""
                <div style="margin: {SPACING['md']} 0;">
                    <div style="font-size: 0.8125rem; font-weight: 600; color: {COLORS['text_primary']};">
                        Voice Enrollment (Optional)
                    </div>
                    <div style="font-size: 0.75rem; color: {COLORS['text_secondary']};">
                        Record your voice for voice-based attendance
                    </div>
                </div>
            """, unsafe_allow_html=True)

            audio_data = None

            try:
                audio_data = st.audio_input('Record "I am present"')
            except Exception:
                st.error('❌ Audio recording failed')

            if st.button('Create Student Profile', type='primary', width='stretch', icon=':material/person_add:'):
                if new_name:
                    with st.spinner('🔧 Creating your profile...'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)

                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'✅ Profile created! Welcome, {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('❌ Could not capture facial features. Please ensure good lighting.')
                else:
                    st.warning('⚠️ Please enter your name')

    footer_dashboard()
