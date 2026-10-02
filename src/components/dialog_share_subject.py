"""
Share Subject Dialog - macOS Style
"""

import streamlit as st
import segno
import io
from src.ui.macos_design_system import COLORS, SPACING, RADIUS


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    """Dialog for sharing subject join link and QR code"""

    app_domain = "snapclass-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.markdown(f"""
        <style>
        .share-header {{
            margin-bottom: {SPACING['lg']};
        }}
        .share-header h3 {{
            margin: 0;
            color: {COLORS['text_primary']};
        }}
        .share-header p {{
            margin: {SPACING['xs']} 0 0 0;
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
        }}
        </style>
        <div class="share-header">
            <h3>{subject_name}</h3>
            <p>Students can scan the QR code or use the code below to join</p>
        </div>
    """, unsafe_allow_html=True)

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=8, border=2)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown(f"<h4 style='font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: {SPACING['xs']};'>Class Code</h4>", unsafe_allow_html=True)
        st.code(subject_code, language="text")

        st.markdown(f"<h4 style='font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: {SPACING['xs']};'>Direct Link</h4>", unsafe_allow_html=True)
        st.code(join_url, language="text")

        st.info("💡 Share this link via WhatsApp, Email, or Slack")

    with col2:
        st.markdown(f"<h4 style='font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: {SPACING['xs']}; text-align: center;'>QR Code</h4>", unsafe_allow_html=True)
        st.image(out.getvalue(), use_container_width=True)
