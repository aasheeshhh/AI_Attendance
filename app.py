import streamlit as st

from src import ui
from src.views import home, student, teacher

ui.setup()

if code := st.query_params.get("join-code"):  # arrived via a class share link
    st.session_state.join_code = code
    st.session_state.portal = "student"
    st.query_params.clear()

{None: home, "teacher": teacher, "student": student}[st.session_state.get("portal")].show()
