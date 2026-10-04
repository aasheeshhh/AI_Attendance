# SnapClass — AI Attendance

Take attendance from a classroom photo or a voice recording. Teachers manage classes and review
results; students sign in with Face ID and track their attendance.

Built with Streamlit, Supabase, dlib (faces) and Resemblyzer (voices).

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your Supabase credentials to `.streamlit/secrets.toml` (git-ignored) or environment variables:

```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "your-key"
APP_URL = "https://your-app.streamlit.app"   # optional, used for class share links
```

## Layout

```
app.py              entry point + routing
src/
  db.py             Supabase queries
  face.py voice.py  recognition
  ui.py             stylesheet + shared components
  dialogs.py        modal dialogs
  views/            home, teacher, student screens
.streamlit/config.toml   theme
```

## Tables

`teachers`, `students` (with `face_embedding`, `voice_embedding`), `subjects`,
`subject_students`, `attendance_logs`.
