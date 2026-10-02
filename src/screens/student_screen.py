"""
Student Screen - macOS Style
Student dashboard with FaceID login and subject enrollment
Preserving all existing functionality with new macOS visual design
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


def student_screen():
    """Main student screen router"""

    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    student_screen_login()


def student_dashboard():
    """Student dashboard - view enrolled subjects and attendance"""

    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # Header with logout
    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        st.markdown(f"""
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: {COLORS['text_tertiary']};">Logged in as</div>
                <div style="font-size: 0.9375rem; font-weight: 600; color: {COLORS['text_primary']};">{student_data['name']}</div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", type='secondary', key='student_logout', shortcut="control+backspace", icon=':material/logout:'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Enrolled subjects header
    c1, c2 = st.columns([3, 1], vertical_alignment='bottom')

    with c1:
        st.markdown(f"""
            <div style="margin-bottom: {SPACING['lg']};">
                <h2 style="margin-bottom: {SPACING['xs']};">Your Subjects</h2>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.9375rem;">
                    Subjects you're enrolled in
                </p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch', icon=':material/add:'):
            enroll_dialog()

    st.divider()

    # Load subjects and attendance data
    with st.spinner('Loading your enrolled subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

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
                        ('📅', 'Classes', stats['total']),
                        ('✅', 'Attended', stats['attended']),
                        ('📊', 'Rate', f"{attendance_pct:.0f}%"),
                    ],
                    footer_callback=unenroll_button
                )
    else:
        st.info("📚 You're not enrolled in any subjects yet. Use the 'Enroll in Subject' button above to join a class.")

    footer_dashboard()


def student_screen_login():
    """Student login screen with FaceID"""

    c1, c2 = st.columns([3, 1], vertical_alignment='center')

    with c1:
        header_dashboard()

    with c2:
        if st.button("← Back to Home", type='secondary', key='studentbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # FaceID login in centered container
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: {SPACING['xl']};">
                <h2>Student Login</h2>
                <p style="color: {COLORS['text_secondary']};">Sign in with Face ID</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <style>
            .faceid-container {{
                background: {COLORS['surface_primary']};
                border: 2px dashed {COLORS['border']};
                border-radius: {RADIUS['lg']};
                padding: {SPACING['xl']};
                text-align: center;
                margin-bottom: {SPACING['lg']};
            }}

            .faceid-icon {{
                font-size: 3rem;
                color: {COLORS['text_tertiary']};
                margin-bottom: {SPACING['md']};
            }}

            .faceid-instruction {{
                font-size: 0.875rem;
                color: {COLORS['text_secondary']};
            }}
            </style>
        """, unsafe_allow_html=True)

        show_registration = False
        photo_source = st.camera_input("Position your face in the frame")

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
                        st.info('🆕 Face not recognized. You might be a new student!')
                        show_registration = True

        if show_registration:
            st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background: {COLORS['surface_secondary']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; margin-bottom: {SPACING['md']};">
                    <h3>Create New Student Profile</h3>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                        Register your face and voice for attendance tracking
                    </p>
                </div>
            """, unsafe_allow_html=True)

            new_name = st.text_input("Full Name", placeholder='Enter your full name', label_visibility='collapsed')

            st.markdown(f"""
                <div style="margin: {SPACING['lg']} 0;">
                    <h4 style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']};">
                        Voice Enrollment (Optional)
                    </h4>
                    <p style="font-size: 0.8125rem; color: {COLORS['text_secondary']};">
                        Record your voice for voice-based attendance
                    </p>
                </div>
            """, unsafe_allow_html=True)

            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like "I am present" or "My name is [Your Name]"')
            except Exception:
                st.error('❌ Audio recording failed')

            if st.button('Create Account', type='primary', width='stretch', icon=':material/person_add:'):
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
                            st.error('❌ Could not capture your facial features. Please try again with better lighting.')
                else:
                    st.warning('⚠️ Please enter your name')

    footer_dashboard()
