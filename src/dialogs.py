"""All modal dialogs."""
import io
import os
from datetime import datetime

import pandas as pd
import segno
import streamlit as st

from src import db, voice

APP_URL = os.getenv("APP_URL", "https://snapclass-main.streamlit.app")


# ── Attendance review (shared by face + voice flows) ────────
def clear_photos():
    st.session_state.photos = {}
    st.session_state.upload_key = st.session_state.get("upload_key", 0) + 1


def start_review(subject_id, roster, present_ids):
    """Stage attendance for review. Returns False if the class has no students."""
    if not roster:
        st.warning("No students are enrolled in this class yet.")
        return False
    st.session_state.pending = {
        "subject_id": subject_id,
        "df": pd.DataFrame({
            "Name": [s["name"] for s in roster],
            "ID": [s["student_id"] for s in roster],
            "Present": [s["student_id"] in present_ids for s in roster],
        }),
    }
    return True


def _finish():
    st.session_state.pop("pending", None)
    clear_photos()
    st.rerun()


def _review():
    pending = st.session_state.pending
    st.caption("Tick or untick anyone the AI got wrong, then save.")
    df = st.data_editor(pending["df"], hide_index=True, width="stretch",
                        disabled=["Name", "ID"], key="review_table")
    st.markdown(f"**{df['Present'].sum()} / {len(df)}** present")

    discard, save = st.columns(2)
    if discard.button("Discard", width="stretch"):
        _finish()
    if save.button("Save", type="primary", icon=":material/check:", width="stretch"):
        now = datetime.now().isoformat(timespec="seconds")
        db.save_attendance([
            {"student_id": int(r.ID), "subject_id": pending["subject_id"],
             "timestamp": now, "is_present": bool(r.Present)}
            for r in df.itertuples()
        ])
        st.toast("Attendance saved")
        _finish()


@st.dialog("Review attendance")
def review_dialog():
    _review()


@st.dialog("Voice attendance")
def voice_dialog(subject_id):
    if "pending" in st.session_state:
        return _review()

    st.caption("Record students saying “I am present”. Each voice is matched to a profile.")
    audio = st.audio_input("Classroom audio", label_visibility="collapsed")
    if not st.button("Analyze", type="primary", icon=":material/graphic_eq:",
                     width="stretch", disabled=audio is None):
        return

    roster = db.get_enrolled(subject_id)
    voices = {s["student_id"]: s["voice_embedding"] for s in roster if s.get("voice_embedding")}
    if not voices:
        return st.error("None of the enrolled students have a voice profile.")
    try:
        with st.spinner("Analyzing audio…"):
            matches = voice.identify(audio.getvalue(), voices)
    except RuntimeError as e:
        return st.error(str(e))
    if start_review(subject_id, roster, set(matches)):
        st.rerun(scope="fragment")


# ── Classes ─────────────────────────────────────────────────
@st.dialog("New class")
def create_subject_dialog(teacher_id):
    with st.form("new_class", border=False):
        code = st.text_input("Code", placeholder="CS101")
        name = st.text_input("Name", placeholder="Intro to Computer Science")
        section = st.text_input("Section", placeholder="A")
        if st.form_submit_button("Create", type="primary", width="stretch"):
            if not (code and name and section):
                return st.warning("Please fill in every field.")
            try:
                db.create_subject(code.strip(), name.strip(), section.strip(), teacher_id)
            except Exception:
                return st.error("Couldn't create the class. That code may already exist.")
            st.toast("Class created")
            st.rerun()


@st.dialog("Share class")
def share_dialog(name, code):
    url = f"{APP_URL}/?join-code={code}"
    qr = io.BytesIO()
    segno.make(url).save(qr, kind="png", scale=8, border=2)

    st.markdown(f"**{name}**")
    st.caption("Students can scan the QR code or open the link to join.")
    left, right = st.columns(2, vertical_alignment="center")
    with left:
        st.caption("Code")
        st.code(code, language=None)
        st.caption("Link")
        st.code(url, language=None)
    right.image(qr.getvalue())


@st.dialog("Join a class")
def enroll_dialog(code=""):
    code = st.text_input("Class code", value=code, placeholder="CS101").strip()
    if st.button("Join", type="primary", width="stretch", disabled=not code):
        subject = db.find_subject(code)
        if not subject:
            return st.error("No class found with that code.")
        if not db.enroll(st.session_state.student["student_id"], subject["subject_id"]):
            return st.info("You're already in this class.")
        st.toast(f"Joined {subject['name']}")
        st.rerun()
