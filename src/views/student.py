from collections import defaultdict
from hashlib import sha256
from io import BytesIO

import numpy as np
import streamlit as st
from PIL import Image

from src import db, face, voice
from src.dialogs import enroll_dialog
from src.ui import back, class_card, topbar


def show():
    student = st.session_state.get("student")
    if student:
        _dashboard(student)
    else:
        _login()


# ── Face ID sign-in / registration ──────────────────────────
def _login():
    back()
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.title("Face ID")
        st.caption("Look at the camera to sign in. New here? We'll set up your profile.")
        photo = st.camera_input("Face", label_visibility="collapsed")
        if not photo:
            return

        image = np.array(Image.open(photo).convert("RGB"))
        key = sha256(photo.getvalue()).hexdigest()
        if st.session_state.get("scan_key") != key:  # scan each photo once, not on every rerun
            try:
                with st.spinner("Scanning…"):
                    st.session_state.scan = face.identify(image)
            except RuntimeError as e:
                return st.error(str(e))
            st.session_state.scan_key = key
        ids, count = st.session_state.scan

        if count == 0:
            return st.warning("No face detected. Try again with better lighting.")
        if count > 1:
            return st.warning("Please make sure only one person is in the frame.")
        if ids and (student := db.get_student(next(iter(ids)))):
            st.session_state.student = student
            st.rerun()

        st.info("We don't recognise you yet. Create your profile:")
        _register(image)


def _register(image):
    name = st.text_input("Full name")
    st.caption("Optional: record “I am present” so voice attendance works for you.")
    audio = st.audio_input("Voice sample", label_visibility="collapsed")

    if st.button("Create profile", type="primary", width="stretch", disabled=not name.strip()):
        with st.spinner("Creating your profile…"):
            voice_embedding = None
            if audio:
                try:
                    voice_embedding = voice.embed(audio.getvalue())
                except Exception:
                    st.warning("Couldn't process the voice sample, so it was skipped.")
            student = db.create_student(name.strip(), face.embeddings(image)[0].tolist(),
                                        voice_embedding)
            face.refresh_gallery()
        st.session_state.student = student
        st.rerun()


# ── Dashboard ───────────────────────────────────────────────
def _dashboard(student):
    subjects = db.get_student_subjects(student["student_id"])
    logs = db.get_student_logs(student["student_id"])

    per_class = defaultdict(lambda: [0, 0])  # subject_id -> [sessions, attended]
    for log in logs:
        per_class[log["subject_id"]][0] += 1
        per_class[log["subject_id"]][1] += bool(log["is_present"])
    sessions = sum(s for s, _ in per_class.values())
    attended = sum(a for _, a in per_class.values())

    topbar("student", f"Hello, {student['name'].split()[0]}", "Your classes and attendance")

    cols = st.columns(3)
    cols[0].metric("Classes", len(subjects))
    cols[1].metric("Attended", f"{attended} / {sessions}")
    cols[2].metric("Attendance rate", f"{attended / sessions:.0%}" if sessions else "–")

    st.write("")
    left, right = st.columns([4, 1], vertical_alignment="center")
    left.subheader("Your classes")
    if right.button("Join class", icon=":material/add:", type="primary", width="stretch"):
        enroll_dialog()
    if code := st.session_state.pop("join_code", None):  # opened from a share link
        enroll_dialog(code)

    if not subjects:
        return st.info("You haven't joined any classes yet. Tap “Join class” and enter a code.")

    for col, subject in zip(st.columns(2) * len(subjects), subjects):
        total, present = per_class[subject["subject_id"]]
        with col, class_card(subject, {"Sessions": total, "Attended": present,
                                       "Rate": f"{present / total:.0%}" if total else "–"}):
            st.button("Leave", key=f"leave{subject['subject_id']}", type="tertiary",
                      icon=":material/logout:", width="stretch", on_click=db.unenroll,
                      args=(student["student_id"], subject["subject_id"]))
