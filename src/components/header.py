import base64
from pathlib import Path

import streamlit as st


LOGO_FILE = Path(__file__).resolve().parents[2] / "assets" / "ai-attendance-logo.jpeg"


@st.cache_data(show_spinner=False)
def get_logo() -> str:
    """Return the project logo as a browser-safe image URL."""
    image_data = base64.b64encode(LOGO_FILE.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{image_data}"


def show_header():
    """Show the AI Attendance logo and name."""
    logo = get_logo()
    st.markdown(
        f"""
        <div class="brand-header">
            <div class="brand-logo-frame">
                <img src="{logo}" alt="AI Attendance logo">
            </div>
            <div class="brand-name">AI Attendance</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
