# ATS-resume-Analyzer

An intelligent web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). This tool analyzes your resume against a job description, provides an ATS compatibility score, and offers actionable feedback to improve your chances of landing an interview.

<img width="1395" height="856" alt="Screenshot 2025-09-13 005940" src="https://github.com/user-attachments/assets/07062ce3-ce00-48d4-81a7-a8ff6cea6a01" />


## Features

-   **ATS Compatibility Score:** Get an instant score (0-100%) indicating how well your resume matches the job description.
-   **Keyword Analysis:** Identifies matching and missing keywords to help you tailor your resume.
-   **Semantic Similarity:** Uses advanced NLP models to measure the contextual relevance of your resume to the job description.
-   **Actionable Feedback:** Provides personalized suggestions to improve your resume's ATS performance.
-   **Multi-Format Support:** Upload resumes in `.pdf`, `.docx`, and `.txt` formats.
-   **Dark Mode:** Sleek and modern user interface with a dark theme for a comfortable user experience.
-   **Analysis History:** (Optional Feature) Keep track of your past analyses to monitor your progress.

## Tech Stack

-   **Backend:** Django, Python
-   **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
-   **NLP & Machine Learning:**
    -   **spaCy:** For natural language processing, including text extraction and keyword analysis.
    -   **Sentence-Transformers:** For calculating semantic similarity between the resume and job description.
-   **Database:** PostgreSQL (for production), SQLite (for development)
-   **Deployment:** Render, Gunicorn, Whitenoise

## Project Structure

ATS_RESUME/

├── ats_optimizer/ # Django project settings

├── analyzer/ # Main Django app

│ ├── forms/ # Form definitions

│ ├── models.py # Database models

│ ├── services.py # Business logic for resume analysis

│ ├── utils/ # NLP and text extraction utilities

│ ├── views/ # Views to handle requests

│ └── urls.py # App-level URL routing

├── static/ # CSS, JS, and image files

├── templates/ # HTML templates

└── manage.py

### Prerequisites

-   Python 3.8+
-   pip (Python package installer)
-   A virtual environment tool (like `venv`)
