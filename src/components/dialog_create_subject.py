"""
Create Subject Dialog - macOS Style
"""

import streamlit as st
from src.database.db import create_subject
from src.ui.macos_design_system import COLORS, SPACING


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    """Dialog for creating a new subject/course"""

    st.markdown(f"""
        <style>
        .dialog-description {{
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
            margin-bottom: {SPACING['lg']};
        }}
        </style>
        <p class="dialog-description">Enter the details for your new subject</p>
    """, unsafe_allow_html=True)

    sub_id = st.text_input("Subject Code", placeholder="e.g., CS101", label_visibility='visible')
    sub_name = st.text_input("Subject Name", placeholder="e.g., Introduction to Computer Science", label_visibility='visible')
    sub_section = st.text_input("Section", placeholder="e.g., A", label_visibility='visible')

    st.markdown(f"<div style='height: {SPACING['md']};'></div>", unsafe_allow_html=True)

    if st.button("Create Subject", type='primary', width='stretch', icon=':material/add:'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("✅ Subject created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Please fill all the fields")
