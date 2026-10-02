"""
Attendance Results Dialog - macOS Style
"""

import streamlit as st
from src.database.db import create_attendance
from src.ui.macos_design_system import COLORS, SPACING, RADIUS


def show_attendance_result(df, logs):
    """Render attendance results table with confirm/discard actions"""

    st.markdown(f"""
        <style>
        .result-header {{
            margin-bottom: {SPACING['md']};
        }}
        .result-header h3 {{
            margin: 0;
            color: {COLORS['text_primary']};
        }}
        .result-header p {{
            margin: {SPACING['xs']} 0 0 0;
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
        }}
        </style>
        <div class="result-header">
            <h3>Attendance Summary</h3>
            <p>Review the detected attendance before saving</p>
        </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown(f"<div style='height: {SPACING['lg']};'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button('Discard', width='stretch', type='secondary', icon=':material/close:'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.session_state.pop('attendance_image_hashes', None)
            st.session_state.pop('dialog_cam', None)
            st.session_state.pop('dialog_upload', None)
            st.rerun()

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary', icon=':material/check:'):
            try:
                create_attendance(logs)
                st.toast("✅ Attendance saved successfully!")
                st.session_state.attendance_images = []
                st.session_state.pop('attendance_image_hashes', None)
                st.session_state.pop('dialog_cam', None)
                st.session_state.pop('dialog_upload', None)
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error('❌ Failed to save attendance')


@st.dialog("Attendance Results")
def attendance_result_dialog(df, logs):
    """Dialog wrapper for attendance results"""
    show_attendance_result(df, logs)
