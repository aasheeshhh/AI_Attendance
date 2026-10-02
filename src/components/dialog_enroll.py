"""
Enroll in Subject Dialog - macOS Style
"""

import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import require_supabase
from src.ui.macos_design_system import COLORS, SPACING

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    """Dialog for students to enroll in a subject using a code"""

    st.markdown(f"""
        <style>
        .enroll-instructions {{
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
            margin-bottom: {SPACING['lg']};
        }}
        </style>
        <p class="enroll-instructions">Enter the subject code provided by your teacher to enroll</p>
    """, unsafe_allow_html=True)

    join_code = st.text_input('Subject Code', placeholder='e.g., CS101', label_visibility='visible')

    st.markdown(f"<div style='height: {SPACING['sm']};'></div>", unsafe_allow_html=True)

    if st.button('Enroll Now', type='primary', width='stretch', icon=':material/add_circle:'):
        if join_code:
            supabase = require_supabase()
            res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', join_code).execute()

            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

                if check.data:
                    st.warning('⚠️ You are already enrolled in this subject')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success(f'✅ Successfully enrolled in {subject["name"]}!')
                    time.sleep(1)
                    st.rerun()
            else:
                st.error('❌ Subject code not found. Please check and try again.')
        else:
            st.warning('⚠️ Please enter a subject code')
