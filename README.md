# StatisticallyUOS

A stats-based leaderboard and teacher review platform for **University of Sindh** students — built to make academic data transparent, accessible, and useful.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat&logo=postgresql&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=flat&logo=next.js&logoColor=white)

---

## Features

- 🏆 **All-time subject leaderboard** — see top performers across every subject
- 📊 **CGPA leaderboard** — overall university rankings
- 🧑‍🏫 **Teacher reviews** — student-submitted feedback on faculty
- 📈 **Subject statistics** — grade distributions and performance trends
- 🔄 **Live data** — continuously updated via automated scraping

---

## Tech Stack

| Layer | Technology |
|---|---|
| Scraping | Python, Requests, BeautifulSoup4 |
| API | FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | HTML, CSS, Next.js |
| Hosting | DigitalOcean VPS |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│             University of Sindh Website      │
└──────────────────────┬──────────────────────┘
                       │ Requests + BeautifulSoup4
                       ▼
┌─────────────────────────────────────────────┐
│           Scraping Script (VPS Cron)         │
│         Runs continuously, auto-updates      │
└──────────────────────┬──────────────────────┘
                       │ Millions of records
                       ▼
┌─────────────────────────────────────────────┐
│              PostgreSQL Database             │
│     Students · Results · Reviews · Stats     │
└──────────────────────┬──────────────────────┘
                       │ SQLAlchemy ORM
                       ▼
┌─────────────────────────────────────────────┐
│              FastAPI Backend (VPS)           │
│   Leaderboards · Subject Stats · Reviews     │
└──────────────────────┬──────────────────────┘
                       │ REST API
                       ▼
┌─────────────────────────────────────────────┐
│            Next.js Frontend                  │
│         Built by Abdul Rehman                │
└─────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Node.js 18+

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/Shahzad-Nizamani/project_usindh.git
cd project_usindh

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Running the Scraper

```bash
python scraper/main.py
```

> **Note:** The scraper is designed to run continuously on a VPS via a cron job or process manager like `supervisor` or `pm2`.

---

## API Overview

The backend exposes REST APIs for:

- `GET /leaderboard/subject/{subject_id}` — subject-wise top students
- `GET /leaderboard/cgpa` — overall CGPA rankings
- `GET /stats/subject/{subject_id}` — grade distribution for a subject
- `GET /reviews/teacher/{teacher_id}` — reviews for a teacher
- `POST /reviews/teacher/{teacher_id}` — submit a teacher review

Full API documentation is available at `/docs` (Swagger UI) when the server is running.

---

## Database

PostgreSQL stores millions of scraped records including:

- Student profiles and enrollment data
- Result records per semester and subject
- Computed CGPA and ranking data
- Teacher review submissions

---

## Deployment

Both the FastAPI backend and the scraping script are hosted on a **DigitalOcean VPS**. The scraper runs on a schedule to keep data up to date. The frontend is deployed separately.

---

## Contributors

| Name | Role |
|---|---|
| [Shahzad Nizamani](https://github.com/Shahzad-Nizamani) | Backend, Database, Scraping, DevOps |
| Abdul Rehman Nizamani (https://github.com/ABDULRNizamani) | Frontend (Next.js) |

---

## License

This project is intended for educational use by University of Sindh students. All scraped data is publicly available on the university's official website.

---

> Built with 💙 for University of Sindh students
