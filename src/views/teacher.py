from datetime import datetime
from hashlib import sha256
from io import BytesIO

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from src import db, face
from src.dialogs import (clear_photos, create_subject_dialog, review_dialog, share_dialog,
                         start_review, voice_dialog)
from src.ui import back, class_card, topbar


def show():
    teacher = st.session_state.get("teacher")
    if teacher:
        _dashboard(teacher)
    else:
        _login()


# ── Auth ────────────────────────────────────────────────────
def _login():
    back()
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.title("Teacher")
        sign_in, register = st.tabs(["Sign in", "Create account"])

        with sign_in, st.form("sign_in", border=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign in", type="primary", width="stretch"):
                teacher = db.teacher_login(username.strip(), password) if username and password else None
                if not teacher:
                    return st.error("Invalid username or password.")
                st.session_state.teacher = teacher
                st.rerun()

        with register, st.form("register", border=False):
            name = st.text_input("Full name")
            username = st.text_input("Choose a username")
            password = st.text_input("Choose a password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            if st.form_submit_button("Create account", type="primary", width="stretch"):
                if not (name and username and password):
                    st.error("Please fill in every field.")
                elif password != confirm:
                    st.error("Passwords don't match.")
                elif not db.create_teacher(username.strip(), password, name.strip()):
                    st.error("That username is taken.")
                else:
                    st.success("Account created. You can sign in now.")


# ── Dashboard ───────────────────────────────────────────────
def _dashboard(teacher):
    subjects = db.get_subjects(teacher["teacher_id"])
    topbar("teacher", f"Hello, {teacher['name'].split()[0]}", datetime.now().strftime("%A, %B %d"))

    cols = st.columns(3)
    cols[0].metric("Classes", len(subjects))
    cols[1].metric("Enrolled students", sum(s["students"] for s in subjects))
    cols[2].metric("Sessions taken", sum(s["sessions"] for s in subjects))

    attendance, classes, records = st.tabs(["Attendance", "Classes", "Records"])
    with attendance:
        _attendance(subjects)
    with classes:
        _classes(teacher, subjects)
    with records:
        _records(teacher)


def _attendance(subjects):
    if not subjects:
        return st.info("Create a class in the Classes tab to start taking attendance.")

    subject = st.selectbox("Class", subjects,
                           format_func=lambda s: f"{s['name']} · {s['subject_code']}")

    photos = st.session_state.setdefault("photos", {})
    n = st.session_state.get("upload_key", 0)
    source = st.segmented_control("Add photos", ["Upload", "Camera"], default="Upload")
    if source == "Camera":
        shot = st.camera_input("Take a photo", key=f"cam{n}", label_visibility="collapsed")
        files = [shot] if shot else []
    else:
        files = st.file_uploader("Photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True,
                                 key=f"up{n}", label_visibility="collapsed")
    for f in files:
        photos[sha256(f.getvalue()).hexdigest()] = f.getvalue()

    if photos:
        st.image([Image.open(BytesIO(b)) for b in photos.values()], width=110)

    clear, scan, voice = st.columns(3)
    if clear.button("Clear photos", icon=":material/delete:", width="stretch", disabled=not photos):
        clear_photos()
        st.rerun()
    if scan.button("Scan faces", type="primary", icon=":material/face:", width="stretch",
                   disabled=not photos):
        _scan_faces(subject["subject_id"], photos)
    if voice.button("Voice attendance", icon=":material/mic:", width="stretch"):
        st.session_state.pop("pending", None)
        voice_dialog(subject["subject_id"])


def _scan_faces(subject_id, photos):
    present, total = set(), 0
    try:
        with st.spinner("Scanning faces…"):
            for data in photos.values():
                ids, count = face.identify(np.array(Image.open(BytesIO(data)).convert("RGB")))
                present |= ids
                total += count
    except RuntimeError as e:
        return st.error(str(e))
    if not total:
        return st.warning("No faces were detected. Try clearer photos.")
    if start_review(subject_id, db.get_enrolled(subject_id), present):
        review_dialog()


def _classes(teacher, subjects):
    if st.button("New class", icon=":material/add:", type="primary"):
        create_subject_dialog(teacher["teacher_id"])
    if not subjects:
        return st.info("No classes yet.")

    for col, subject in zip(st.columns(2) * len(subjects), subjects):
        with col, class_card(subject, {"Students": subject["students"],
                                       "Sessions": subject["sessions"]}):
            if st.button("Share", key=f"share{subject['subject_id']}", icon=":material/share:",
                         width="stretch"):
                share_dialog(subject["name"], subject["subject_code"])


def _records(teacher):
    logs = db.get_teacher_logs(teacher["teacher_id"])
    if not logs:
        return st.info("No attendance recorded yet.")

    df = pd.DataFrame({
        "when": [log["timestamp"][:19] for log in logs],
        "Class": [log["subjects"]["name"] for log in logs],
        "Code": [log["subjects"]["subject_code"] for log in logs],
        "present": [bool(log["is_present"]) for log in logs],
    })
    sessions = (df.groupby(["when", "Class", "Code"]).present.agg(["sum", "count"])
                .reset_index().sort_values("when", ascending=False))
    sessions["Date"] = pd.to_datetime(sessions["when"]).dt.strftime("%b %d, %Y · %I:%M %p")
    sessions["Present"] = sessions["sum"].astype(str) + " / " + sessions["count"].astype(str)
    sessions["Rate"] = sessions["sum"] / sessions["count"] * 100

    st.dataframe(sessions[["Date", "Class", "Code", "Present", "Rate"]], hide_index=True,
                 width="stretch",
                 column_config={"Rate": st.column_config.ProgressColumn(
                     format="%.0f%%", min_value=0, max_value=100)})
