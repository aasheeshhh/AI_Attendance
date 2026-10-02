import os
from typing import Any

try:
    import streamlit as st
except ImportError:  # pragma: no cover - Streamlit is required at runtime.
    st = None

try:
    from supabase import create_client
except ImportError:  # pragma: no cover - optional runtime dependency
    create_client = None


def _get_secrets_value(key):
    value = None
    if st is not None and hasattr(st, "secrets"):
        try:
            value = st.secrets.get(key)
        except Exception:
            pass
    return value or os.getenv(key)


SUPABASE_URL = _get_secrets_value("SUPABASE_URL")
SUPABASE_KEY = _get_secrets_value("SUPABASE_KEY")

supabase: Any = None
if SUPABASE_URL and SUPABASE_KEY and create_client is not None:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def require_supabase():
    if supabase is None:
        raise RuntimeError(
            "Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY to environment variables or Streamlit secrets."
        )
    return supabase