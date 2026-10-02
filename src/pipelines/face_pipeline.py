try:
    import dlib
except ImportError:  # pragma: no cover - optional runtime dependency
    dlib = None

import numpy as np

try:
    import face_recognition_models
except ImportError:  # pragma: no cover - optional runtime dependency
    face_recognition_models = None

try:
    from sklearn.svm import SVC
except ImportError:  # pragma: no cover - optional runtime dependency
    SVC = None

try:
    import streamlit as st
except ImportError:  # pragma: no cover - optional runtime dependency
    st = None

try:
    from src.database.db import get_all_students
except Exception:  # pragma: no cover - runtime database dependency
    def get_all_students():
        return []

RESEMBLANCE_THRESHOLD = 0.6

if st is not None:
    cache_resource = st.cache_resource
else:
    def cache_resource(func):
        return func


@cache_resource
def load_dlib_models():
    if dlib is None or face_recognition_models is None:
        raise ModuleNotFoundError(
            'The face recognition dependencies are missing. Install dlib and face_recognition_models.'
        )

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def _normalize_embedding(embedding):
    if embedding is None:
        return None

    try:
        embedding_array = np.asarray(embedding, dtype=float).reshape(-1)
    except (TypeError, ValueError):
        return None

    if embedding_array.size != 128 or not np.isfinite(embedding_array).all():
        return None

    return embedding_array


def get_face_embeddings(image_np):
    if image_np is None:
        return []

    image_array = np.asarray(image_np)
    if image_array.size == 0:
        return []

    try:
        detector, sp, facerec = load_dlib_models()
    except (ModuleNotFoundError, RuntimeError):
        return []

    faces = detector(image_array, 1)
    encodings = []

    for face in faces:
        try:
            shape = sp(image_array, face)
            face_descriptor = facerec.compute_face_descriptor(image_array, shape, 1)
            embedding = _normalize_embedding(face_descriptor)
            if embedding is not None:
                encodings.append(embedding)
        except Exception:
            continue

    return encodings


def _best_match_for_encoding(encoding, X_train, y_train):
    if not X_train:
        return None, float('inf')

    X_train = [np.asarray(sample, dtype=float).reshape(-1) for sample in X_train]
    candidate_distances = [
        float(np.linalg.norm(sample - np.asarray(encoding, dtype=float).reshape(-1)))
        for sample in X_train
    ]

    if not candidate_distances:
        return None, float('inf')

    best_index = int(np.argmin(candidate_distances))
    return y_train[best_index], candidate_distances[best_index]


@cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students() or []

    for student in student_db:
        student_id = student.get('student_id')
        embedding = _normalize_embedding(student.get('face_embedding'))

        if student_id is None or embedding is None:
            continue

        X.append(embedding)
        y.append(student_id)

    if not X:
        return None

    all_students = sorted(set(y))
    if SVC is None:
        return {'clf': None, 'X': X, 'y': y, 'all_students': all_students}

    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(np.asarray(X), np.asarray(y))
    except ValueError:
        return {'clf': None, 'X': X, 'y': y, 'all_students': all_students}

    return {'clf': clf, 'X': X, 'y': y, 'all_students': all_students}


def train_classifier():
    if st is not None:
        st.cache_resource.clear()
    model_data = get_trained_model()
    return model_data is not None


def predict_attendance(class_image_np):
    if class_image_np is None:
        return {}, [], 0

    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    model_data = get_trained_model()
    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data.get('clf')
    X_train = model_data['X']
    y_train = model_data['y']
    all_students = list(model_data.get('all_students', sorted(set(y_train))))

    if not X_train:
        return detected_student, all_students, len(encodings)

    for encoding in encodings:
        predicted_id = None

        if clf is not None and len(all_students) >= 2:
            try:
                predicted_id = clf.predict([encoding])[0]
            except (AttributeError, ValueError):
                predicted_id = None

        if predicted_id is None:
            predicted_id, best_match_score = _best_match_for_encoding(encoding, X_train, y_train)
            if predicted_id is None:
                continue
        else:
            matching_embeddings = [
                sample for sample, student_id in zip(X_train, y_train)
                if student_id == predicted_id
            ]
            if not matching_embeddings:
                continue
            best_match_score = min(
                float(np.linalg.norm(np.asarray(sample) - encoding))
                for sample in matching_embeddings
            )

        try:
            student_key = int(predicted_id)
        except (TypeError, ValueError):
            student_key = predicted_id

        if best_match_score <= RESEMBLANCE_THRESHOLD:
            detected_student[student_key] = True

    return detected_student, all_students, len(encodings)
