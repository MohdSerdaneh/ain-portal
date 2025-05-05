
# Ain Portal - Sign Language & Emotion Recognition for E-Learning

## Final Year Project - University of Nottingham
**Author:** Mohammed Abusirdaneh  
**GitHub:** [MohdSerdaneh](https://github.com/MohdSerdaneh)  
**Repository:** https://github.com/MohdSerdaneh/ain-portal

---

## Project Overview

**Ain Portal** is a full-stack educational platform tailored for **deaf and hard-of-hearing students**. It integrates **American Sign Language (ASL)** and **facial emotion detection** using **real-time video** and **deep learning** to enhance learning and accessibility.

Built with Django, this platform allows:
- Students to join virtual classrooms, interact with teachers, and take quizzes.
- Teachers to manage courses, students, and evaluate progress using AI insights.
- Real-time ASL detection, space/sentence management, and AI-generated PDF reports.

---

## Key Features

- ASL Detection with gesture holding & sentence construction.
- Emotion Recognition during camera sessions.
- Live Video Meetings powered by Agora.
- Quiz & Course Management for teachers.
- Dashboard Interface for teachers and students.
- Auto-generated Session PDF Reports including engagement charts.
- AI-Driven Feedback for emotion-sentiment alignment.

---

## Folder Structure

```
Ain-Portal/
├── accounts/               # Authentication system
├── adminDashboard/         # Basic admin pages
├── meeting/                # Video & AI detection
│   └── API/                # ASL & Emotion detection scripts
├── quiz/                   # Quizzes and questions
├── student/                # Student dashboards and views
├── teacher/                # Teacher dashboards and views
├── static/                 # CSS, JS, assets
├── templates/              # HTML templates
├── media/                  # Uploaded avatars, reports
├── src/                    # Settings, URLs, middleware
└── db.sqlite3              # Django default database (included)
```

---

## Installation Instructions (Anaconda)

### Step-by-Step Setup

1. **Clone the Repository**:

```bash
git clone https://github.com/MohdSerdaneh/ain-portal.git
cd ain-portal
```

2. **Create and Activate Anaconda Environment**:

```bash
conda create --name ain_env python=3.9
conda activate ain_env
```

3. **Install All Requirements**:

```bash
conda install --file conda_requirements.txt
```

4. **Run Initial Django Setup**:

```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin user
python manage.py collectstatic
```

5. **Start the Server**:

```bash
python manage.py runserver
```

Visit the admin panel at: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)  
Use credentials:
- Username: `admin`
- Password: `admin123`

---

## Using ASL + Emotion Full Pipeline

### Step-by-Step Instructions

From the root of your project:

```bash
cd Portal/Portal/meeting/API
python full_pipeline.py
```

### ASL Instructions

- Hold a **sign** for **1.5 seconds** to register a letter.
- Use **both hands together** to trigger a **space**.
- Remove hands for 4 seconds to **end sentence**.
- Ended sentences are spoken aloud, logged, and sent to chat.

Ensure webcam access and good lighting conditions.

---

## Included Database

- `db.sqlite3` is preconfigured.
- Contains test users, courses, sample content.
- You can wipe and reset via:

```bash
python manage.py flush
```

---

## User Guide

An extensive user guide is provided in a separate `User_Guide_AinPortal.pdf`.  
It includes sections for:
- Student onboarding
- Navigation and feature use
- Course, report, and quiz workflows
- AI detection usage

Place screenshots in `/docs/screenshots/` folder (add yours manually).

---

## Technologies

| Type       | Stack                         |
|------------|-------------------------------|
| Backend    | Django, Django Channels        |
| ML/AI      | TensorFlow, OpenCV, MediaPipe |
| Charts     | Matplotlib, FPDF               |
| Real-time  | Agora, Redis                   |
| Frontend   | Tailwind CSS, HTMX             |
| NLP        | Transformers, TextBlob         |

---

##  License

This project is intended for academic and educational use only.  
For questions or commercial licensing, contact [MohdSerdaneh](https://github.com/MohdSerdaneh).

---

> "Where Signs Speak and Emotions Teach." – Ain Portal
