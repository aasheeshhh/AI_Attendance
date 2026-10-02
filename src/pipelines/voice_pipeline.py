try:
    from resemblyzer import VoiceEncoder, preprocess_wav
except ImportError:  # pragma: no cover - optional runtime dependency
    VoiceEncoder = None
    preprocess_wav = None

import io
import numpy as np

try:
    import librosa
except ImportError:  # pragma: no cover - optional runtime dependency
    librosa = None

try:
    import streamlit as st
except ImportError:  # pragma: no cover - optional runtime dependency
    st = None


if st is not None:
    cache_resource = st.cache_resource
else:
    def cache_resource(func):
        return func


@cache_resource
def load_voice_encoder():
    if VoiceEncoder is None or preprocess_wav is None:
        raise ModuleNotFoundError(
            'The voice recognition dependencies are missing. Install resemblyzer and librosa.'
        )
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    if audio_bytes is None or librosa is None or VoiceEncoder is None or preprocess_wav is None:
        return None

    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception:
        if st is not None:
            st.error('Voice recog error')
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    if audio_bytes is None or librosa is None or VoiceEncoder is None or preprocess_wav is None:
        if st is not None:
            st.error('Voice recognition dependencies are not available.')
        return None

    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception:
        if st is not None:
            st.error('Bulk process error')
        return None