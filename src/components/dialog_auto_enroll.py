"""
Auto Enroll Dialog - macOS Style
Quick enrollment from URL join code
"""

import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import require_supabase
from src.ui.macos_design_system import COLORS, SPACING, RADIUS

import time


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    """Auto-enrollment dialog triggered by URL join code"""

    student_id = st.session_state.student_data['student_id']

    supabase = require_supabase()
    res = supabase.table('subjects').select('subject_id, name').eq('subject_code', subject_code).execute()

    if not res.data:
        st.error('❌ Subject code not found')
        if st.button('Close', width='stretch'):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

    if check.data:
        st.info('ℹ️ You\'re already enrolled in this subject!')
        if st.button('Got it!', width='stretch', type='primary'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"""
        <style>
        .auto-enroll-card {{
            background: {COLORS['surface_secondary']};
            padding: {SPACING['lg']};
            border-radius: {RADIUS['lg']};
            margin-bottom: {SPACING['lg']};
            text-align: center;
        }}
        .subject-name {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['xs']};
        }}
        .enroll-prompt {{
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
        }}
        </style>
        <div class="auto-enroll-card">
            <div class="subject-name">{subject['name']}</div>
            <p class="enroll-prompt">Would you like to enroll in this subject?</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button('No Thanks', width='stretch', type='secondary'):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button('Yes, Enroll!', type='primary', width='stretch', icon=':material/check:'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('✅ Enrolled successfully!')
            st.query_params.clear()
            time.sleep(1)
            st.rerun()
