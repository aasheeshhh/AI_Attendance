"""Voice recognition: Resemblyzer speaker embeddings."""
import io

import numpy as np
import streamlit as st

SAMPLE_RATE = 16000
THRESHOLD = 0.65  # min cosine similarity to count as the same speaker


@st.cache_resource
def _encoder():
    try:
        from resemblyzer import VoiceEncoder
    except ImportError as e:
        raise RuntimeError("Voice recognition needs resemblyzer and librosa.") from e
    return VoiceEncoder()


def _load(audio_bytes):
    import librosa
    return librosa.load(io.BytesIO(audio_bytes), sr=SAMPLE_RATE)[0]


def embed(audio_bytes):
    """Embedding for one speaker's recording, as a plain list."""
    from resemblyzer import preprocess_wav
    return _encoder().embed_utterance(preprocess_wav(_load(audio_bytes))).tolist()


def identify(audio_bytes, candidates):
    """Match each spoken segment to {student_id: embedding}. Returns {student_id: best score}."""
    import librosa
    from resemblyzer import preprocess_wav

    audio, encoder, matches = _load(audio_bytes), _encoder(), {}
    for start, end in librosa.effects.split(audio, top_db=30):
        if end - start < SAMPLE_RATE // 2:  # ignore clips under 0.5s
            continue
        vec = encoder.embed_utterance(preprocess_wav(audio[start:end]))
        sid, score = max(((s, float(np.dot(vec, e))) for s, e in candidates.items()),
                         key=lambda pair: pair[1])
        if score >= THRESHOLD and score > matches.get(sid, 0):
            matches[sid] = score
    return matches
