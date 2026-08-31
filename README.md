# Campus Skill Exchange Platform

## Live Application

🌐 https://web-production-fc8ca.up.railway.app

## Student

Mohammed Rayan Suhuyini — KNUST Computer Science

## Project Description

An AI-powered peer-to-peer skill exchange and mentorship platform
for KNUST students. Students register skills they can teach and
skills they want to learn. The platform uses TF-IDF (NLP) +
Cosine Similarity to intelligently match students with the best
peer tutors. Connected students can chat directly within the platform.

## Tech Stack

- Backend: Django 4.2 (Python)
- Frontend: Bootstrap 5 + Custom CSS
- Database: SQLite (local) / Railway PostgreSQL (production)
- AI: scikit-learn (TF-IDF + Cosine Similarity)
- Authentication: django-allauth (Username + Google OAuth 2.0)
- Deployment: Railway (via GitHub)

## Features

- User registration and login
- Google Sign-In
- Add/delete skills (Teach & Learn)
- AI-powered skill search with relevance scoring
- Peer connection system
- Real-time style chat between connected students
- Light and Dark mode
- Mobile responsive

## Demo Accounts

Username: ama_k | Password: pass123
Username: kofi_b | Password: pass123
Username: esi_m | Password: pass123

## How to Run Locally

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
