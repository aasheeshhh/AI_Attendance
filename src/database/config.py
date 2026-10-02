import os

try:
    import streamlit as st
except ImportError:  # pragma: no cover - Streamlit is required at runtime.
    st = None

try:
    from supabase import create_client, Client
except ImportError:  # pragma: no cover - optional runtime dependency
    create_client = None
    Client = None


def _get_secrets_value(key):
    if st is not None and hasattr(st, "secrets"):
        try:
            return st.secrets.get(key)
        except Exception:
            return None
    return os.getenv(key)


SUPABASE_URL = _get_secrets_value("SUPABASE_URL")
SUPABASE_KEY = _get_secrets_value("SUPABASE_KEY")

supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY and create_client is not None:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def require_supabase():
    if supabase is None:
        raise RuntimeError(
            "Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY to environment variables or Streamlit secrets."
        )
    return supabase