"""Face recognition: dlib embeddings + nearest-neighbour match."""
import numpy as np
import streamlit as st

from src.db import get_students

THRESHOLD = 0.6  # max embedding distance to count as the same person


@st.cache_resource
def _models():
    try:
        import dlib
        import face_recognition_models as m
    except ImportError as e:
        raise RuntimeError("Face recognition needs dlib-bin and face_recognition_models.") from e
    return (dlib.get_frontal_face_detector(),
            dlib.shape_predictor(m.pose_predictor_model_location()),
            dlib.face_recognition_model_v1(m.face_recognition_model_location()))


def embeddings(image):
    """128-d embedding for every face in an RGB numpy image."""
    detector, shape, encoder = _models()
    return [np.array(encoder.compute_face_descriptor(image, shape(image, f), 1))
            for f in detector(image, 1)]


@st.cache_resource
def _gallery():
    ids, vecs = [], []
    for s in get_students():
        vec = np.asarray(s.get("face_embedding") or [], dtype=float)
        if vec.size == 128:
            ids.append(s["student_id"])
            vecs.append(vec)
    return ids, np.array(vecs)


def refresh_gallery():
    """Call after a new student registers."""
    _gallery.clear()


def identify(image):
    """Returns (set of recognised student ids, number of faces found)."""
    faces = embeddings(image)
    ids, vecs = _gallery()
    found = set()
    if ids:
        for face in faces:
            dist = np.linalg.norm(vecs - face, axis=1)
            best = int(dist.argmin())
            if dist[best] <= THRESHOLD:
                found.add(ids[best])
    return found, len(faces)
