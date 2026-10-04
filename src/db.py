"""Supabase data access. One function per query."""
import os

import bcrypt
import streamlit as st
from supabase import create_client


def _secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)


@st.cache_resource
def _db():
    url, key = _secret("SUPABASE_URL"), _secret("SUPABASE_KEY")
    if not (url and key):
        st.error("Supabase isn't configured. Set SUPABASE_URL and SUPABASE_KEY in "
                 ".streamlit/secrets.toml or as environment variables.")
        st.stop()
    return create_client(url, key)


def _table(name):
    return _db().table(name)


# ── Teachers ────────────────────────────────────────────────
def create_teacher(username, password, name):
    """Returns False if the username is taken."""
    if _table("teachers").select("username").eq("username", username).execute().data:
        return False
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    _table("teachers").insert({"username": username, "password": hashed, "name": name}).execute()
    return True


def teacher_login(username, password):
    rows = _table("teachers").select("*").eq("username", username).execute().data
    if rows and bcrypt.checkpw(password.encode(), rows[0]["password"].encode()):
        rows[0].pop("password")
        return rows[0]


# ── Students ────────────────────────────────────────────────
def get_students():
    return _table("students").select("*").execute().data


def get_student(student_id):
    rows = _table("students").select("*").eq("student_id", student_id).execute().data
    return rows[0] if rows else None


def create_student(name, face_embedding, voice_embedding=None):
    data = {"name": name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    return _table("students").insert(data).execute().data[0]


# ── Subjects ────────────────────────────────────────────────
def create_subject(code, name, section, teacher_id):
    _table("subjects").insert(
        {"subject_code": code, "name": name, "section": section, "teacher_id": teacher_id}
    ).execute()


def get_subjects(teacher_id):
    """Teacher's subjects with `students` and `sessions` counts added."""
    rows = (_table("subjects")
            .select("*, subject_students(count), attendance_logs(timestamp)")
            .eq("teacher_id", teacher_id).execute().data)
    for r in rows:
        counts = r.pop("subject_students") or [{}]
        r["students"] = counts[0].get("count", 0)
        r["sessions"] = len({log["timestamp"] for log in r.pop("attendance_logs")})
    return rows


def find_subject(code):
    rows = _table("subjects").select("subject_id, name").eq("subject_code", code).execute().data
    return rows[0] if rows else None


def get_enrolled(subject_id):
    rows = _table("subject_students").select("students(*)").eq("subject_id", subject_id).execute().data
    return [r["students"] for r in rows]


def get_student_subjects(student_id):
    rows = _table("subject_students").select("subjects(*)").eq("student_id", student_id).execute().data
    return [r["subjects"] for r in rows]


def enroll(student_id, subject_id):
    """Returns False if already enrolled."""
    pair = {"student_id": student_id, "subject_id": subject_id}
    if _table("subject_students").select("student_id").match(pair).execute().data:
        return False
    _table("subject_students").insert(pair).execute()
    return True


def unenroll(student_id, subject_id):
    _table("subject_students").delete().match(
        {"student_id": student_id, "subject_id": subject_id}).execute()


# ── Attendance ──────────────────────────────────────────────
def save_attendance(logs):
    _table("attendance_logs").insert(logs).execute()


def get_student_logs(student_id):
    return _table("attendance_logs").select("*").eq("student_id", student_id).execute().data


def get_teacher_logs(teacher_id):
    return (_table("attendance_logs").select("*, subjects!inner(*)")
            .eq("subjects.teacher_id", teacher_id).execute().data)
