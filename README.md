# SnapClass — AI Attendance System

> **AI-powered classroom attendance using face and voice recognition.**

SnapClass is an AI-powered attendance platform that helps teachers manage classes and record attendance using **face recognition or voice recognition**, while students can join classes and track their attendance.

Built with **Python, Streamlit, Supabase, dlib, and Resemblyzer**.

<p align="center">
  <a href="https://ai-attendance-v1.streamlit.app/">🚀 Live Demo</a>
  ·
  <a href="https://github.com/aasheeshhh/AI_Attendance">📦 GitHub Repository</a>
</p>

---

## 📸 Screenshots

### Home

![SnapClass Home](docs/screenshots/home.png)

### Teacher Dashboard

![Teacher Dashboard](docs/screenshots/teacher-dashboard.png)

### AI Face Attendance

![Face Attendance](docs/screenshots/face-attendance.png)

### Attendance Review

![Attendance Review](docs/screenshots/attendance-review.png)

### Student Dashboard

![Student Dashboard](docs/screenshots/student-dashboard.png)

> Screenshots showcase the main application workflow and UI.

---

# ✨ Features

## 👨‍🏫 Teacher Portal

- Teacher account registration and login
- Create and manage classes
- View enrolled students
- Share classes using class codes and QR codes
- Take attendance using classroom photos
- Take attendance using voice recordings
- Review and manually correct AI-generated attendance
- View historical attendance records
- Track class statistics and attendance rates

## 👨‍🎓 Student Portal

- Face-based student identification
- New student profile registration
- Optional voice profile registration
- Join classes using a class code
- Join classes through shared QR links
- View enrolled classes
- Track attendance history
- View attendance percentage
- Leave enrolled classes

## 🤖 AI Recognition

### Face Recognition

SnapClass uses face embeddings to identify students from classroom images.

```text
Classroom Photo
      ↓
Face Detection
      ↓
128-D Face Embedding
      ↓
Compare Against Student Gallery
      ↓
Nearest-Neighbor Matching
      ↓
Distance Threshold
      ↓
Recognized Students

### Voice Recognition

SnapClass can also identify students from classroom audio.


Classroom Audio
      ↓
Speech Segmentation
      ↓
Audio Preprocessing
      ↓
Speaker Embedding
      ↓
Cosine Similarity
      ↓
Similarity Threshold
      ↓
Recognized Students
```

Voice embeddings are generated using **Resemblyzer**.

---

# 🧠 How Attendance Works

## Face Attendance

1. Teacher selects a class.
2. Teacher uploads classroom photos or captures a photo using the camera.
3. SnapClass detects faces in the images.
4. Each detected face is converted into an embedding.
5. Embeddings are compared with registered student embeddings.
6. Recognized students are identified as attendance candidates.
7. Teacher reviews the generated attendance.
8. Teacher can correct incorrect predictions.
9. Final attendance is saved to Supabase.

## Voice Attendance

1. Teacher selects a class.
2. Teacher records classroom audio.
3. Audio is segmented into speech regions.
4. Each segment is converted into a speaker embedding.
5. Speaker embeddings are compared with registered student voice profiles.
6. Matching students are identified.
7. Teacher reviews the results.
8. Final attendance is saved to Supabase.

## Human-in-the-Loop Verification

AI recognition is **not treated as the final authority**.

The teacher receives a review screen where attendance can be corrected before it is permanently saved.

This helps handle recognition errors caused by:

- Poor lighting
- Face occlusion
- Multiple people in a frame
- Background noise
- Recording quality
- Recognition threshold errors

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      SnapClass       │
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
           Teacher Portal    Student Portal     Shared UI
                  │                 │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        Face Engine   Voice Engine   Attendance
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Supabase   │
                    │   Database   │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Students          Subjects       Attendance
                                       Records
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and AI logic |
| **Streamlit** | Web application and UI |
| **Supabase** | Database and backend services |
| **PostgreSQL** | Relational data storage |
| **dlib** | Face detection and face embeddings |
| **face_recognition_models** | Pre-trained face recognition model |
| **Resemblyzer** | Speaker/voice embeddings |
| **librosa** | Audio processing |
| **NumPy** | Numerical and embedding operations |
| **Pandas** | Attendance data processing |
| **bcrypt** | Teacher password hashing |
| **Pillow** | Image processing |
| **Segno** | QR code generation |

---

# 📂 Project Structure

```text
AI_Attendance/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── logo.png
│
├── src/
│   ├── db.py
│   ├── dialogs.py
│   ├── face.py
│   ├── ui.py
│   ├── voice.py
│   │
│   └── views/
│       ├── home.py
│       ├── teacher.py
│       └── student.py
│
├── docs/
│   └── screenshots/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Module Responsibilities

**`app.py`**

Application entry point and portal routing.

**`src/db.py`**

Centralized Supabase data-access functions for:

- Teachers
- Students
- Subjects
- Enrollments
- Attendance records

**`src/face.py`**

Handles:

- Face detection
- Face embedding generation
- Student face gallery
- Face matching

**`src/voice.py`**

Handles:

- Audio preprocessing
- Speaker embedding generation
- Voice matching

**`src/dialogs.py`**

Reusable Streamlit dialogs for:

- Attendance review
- Voice attendance
- Class creation
- Class sharing
- Class enrollment

**`src/views/teacher.py`**

Handles:

- Teacher authentication
- Teacher dashboard
- Class management
- Attendance
- Attendance records

**`src/views/student.py`**

Handles:

- Face-based student login
- Student registration
- Class enrollment
- Attendance tracking

**`src/ui.py`**

Shared UI components, styling, navigation, cards, and layout functionality.

---

# 🗄️ Database Design

SnapClass uses Supabase/PostgreSQL for persistent storage.

## Main Tables

```text
teachers
│
├── teacher_id
├── username
├── password
└── name


students
│
├── student_id
├── name
├── face_embedding
└── voice_embedding


subjects
│
├── subject_id
├── subject_code
├── name
├── section
└── teacher_id


subject_students
│
├── student_id
└── subject_id


attendance_logs
│
├── student_id
├── subject_id
├── timestamp
└── is_present
```

## Relationships

```text
Teacher
   │
   └── 1 ──────── N ─── Subject
                         │
                         │
                         N
                         │
                         1
                    Enrollment
                         │
                         │
                         N
                         │
                      Student
                         │
                         │
                         N
                         │
                  Attendance Log
```

---

# 🔐 Authentication & Security

Teacher authentication uses:

- Username/password authentication
- bcrypt password hashing
- Passwords are not stored as plaintext

Application secrets are kept outside the repository using Streamlit secrets or environment variables.

```text
.streamlit/secrets.toml
```

is excluded from Git using `.gitignore`.

### Environment Variables

```env
SUPABASE_URL=
SUPABASE_KEY=
APP_URL=
```

> Never commit real Supabase credentials or other secrets to GitHub.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/aasheeshhh/AI_Attendance.git
cd AI_Attendance
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Supabase

Create a Supabase project and configure:

```text
SUPABASE_URL
SUPABASE_KEY
APP_URL
```

For Streamlit, create:

```text
.streamlit/secrets.toml
```

Example:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-key"
APP_URL = "https://your-app.streamlit.app"
```

> Keep `secrets.toml` private.

## 5. Start the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 📋 Example Workflow

## Teacher Workflow

```text
Create Teacher Account
        ↓
Create Class
        ↓
Share Class Code / QR
        ↓
Students Join
        ↓
Capture Classroom Photo
        ↓
AI Face Recognition
        ↓
Review Attendance
        ↓
Save Attendance
        ↓
View Attendance Records
```

## Student Workflow

```text
Open Student Portal
        ↓
Face ID
        ↓
Recognized?
   ┌────┴────┐
  Yes        No
   │          │
 Login      Register
   │          │
   └────┬─────┘
        ↓
Join Class
        ↓
View Attendance
```

---

# ⚡ Performance Considerations

The application uses Streamlit resource caching for expensive AI components, including:

- Face recognition models
- Voice encoder
- Face recognition gallery

Caching reduces repeated model loading during Streamlit reruns.

The face gallery is refreshed when a new student registers so that newly created profiles become available for recognition.

---

# ⚠️ Limitations

SnapClass is currently a **portfolio/educational project**, not a production biometric security system.

Current limitations include:

- Face recognition can be affected by lighting, pose, occlusion, and image quality.
- Voice recognition can be affected by background noise and recording quality.
- Recognition thresholds have not been validated on a large representative dataset.
- The system does not currently provide enterprise-grade biometric anti-spoofing.
- Recognition results should be reviewed by the teacher before final attendance is saved.

These limitations would need to be addressed before using the system in a high-stakes production environment.

---

# 🔮 Future Improvements

- [ ] Supabase Row Level Security (RLS)
- [ ] Automated unit and integration tests
- [ ] GitHub Actions CI
- [ ] Multiple face embeddings per student
- [ ] Recognition confidence scores
- [ ] Improved voice matching and noise handling
- [ ] Liveness / anti-spoofing detection
- [ ] Dedicated attendance session model
- [ ] Attendance analytics and visualizations
- [ ] Attendance report export
- [ ] Improved role-based authorization
- [ ] Application logging and monitoring

---

# 🎯 Project Goals

SnapClass was designed to explore how AI-based identity recognition can be integrated into a practical application rather than building a standalone machine-learning demo.

The project combines:

```text
Machine Learning
       +
Web Application
       +
Database
       +
Authentication
       +
Human Verification
       =
Practical AI System
```

---

# 👨‍💻 Author

**Ashish Ligade**

GitHub:  
https://github.com/aasheeshhh

---

# 📄 License

This project is currently intended for educational and portfolio purposes.
```
