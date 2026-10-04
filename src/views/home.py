import streamlit as st

from src.ui import LOGO, go

PORTALS = [
    ("teacher", "Teacher", "Manage classes and take attendance with face or voice recognition."),
    ("student", "Student", "Sign in with Face ID, join classes and track your attendance."),
]


def show():
    with st.container(key="hero"):
        st.image(LOGO, width=88)
        st.title("SnapClass")
        st.caption("AI-powered attendance, made simple.")

    for col, (portal, title, text) in zip(st.columns(2, gap="large"), PORTALS):
        with col, st.container(border=True, key=f"card-{portal}"):
            st.subheader(title)
            st.write(text)
            st.button(f"Continue as {title}", key=f"go-{portal}", type="primary", width="stretch",
                      icon=":material/arrow_forward:", on_click=go, args=(portal,))
