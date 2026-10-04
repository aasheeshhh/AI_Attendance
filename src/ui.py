"""Shared look & feel: one stylesheet and a few small helpers."""
from contextlib import contextmanager

import streamlit as st

LOGO = "assets/logo.png"

CSS = """
<style>
#MainMenu, footer, [data-testid="stDecoration"] { display: none; }
.block-container { max-width: 1000px; padding-top: 3rem; animation: fade-in .35s ease; }
@keyframes fade-in { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

/* no grey flash while Streamlit reruns */
[data-stale="true"] { opacity: 1 !important; transition: none !important; }

button { transition: transform .15s ease, box-shadow .15s ease, background .15s ease !important; }
button:hover:not(:disabled) { transform: translateY(-1px); }
button:active:not(:disabled) { transform: scale(.98); }

[class*="st-key-card"] { transition: box-shadow .2s ease, transform .2s ease; }
[class*="st-key-card"]:hover { box-shadow: 0 6px 20px rgba(0,0,0,.07); transform: translateY(-2px); }
[class*="st-key-card"] [data-testid="stMetricValue"] { font-size: 1.5rem; }

.st-key-hero { text-align: center; margin-bottom: 1.5rem; }
.st-key-hero [data-testid="stImage"] { display: flex; justify-content: center; }
</style>
"""


def setup():
    st.set_page_config(page_title="SnapClass", page_icon=LOGO, layout="wide",
                       initial_sidebar_state="collapsed")
    st.markdown(CSS, unsafe_allow_html=True)


def go(portal):
    """Button callback: open a portal (or None for home)."""
    st.session_state.portal = portal


def back():
    st.button("Back", icon=":material/arrow_back:", type="tertiary", on_click=go, args=(None,))


def topbar(role, title, subtitle):
    """Page heading with a sign-out button. `role` is 'teacher' or 'student'."""
    def sign_out():
        st.session_state.pop(role, None)
        go(None)

    left, right = st.columns([5, 1], vertical_alignment="center")
    with left:
        st.title(title)
        st.caption(subtitle)
    right.button("Sign out", icon=":material/logout:", on_click=sign_out, width="stretch")


@contextmanager
def class_card(subject, stats):
    """Bordered card showing a class and a row of metrics. Put actions in the `with` body."""
    with st.container(border=True, key=f"card-{subject['subject_id']}"):
        st.markdown(f"**{subject['name']}**")
        st.caption(f"`{subject['subject_code']}` · Section {subject['section']}")
        for col, (label, value) in zip(st.columns(len(stats)), stats.items()):
            col.metric(label, value)
        yield
