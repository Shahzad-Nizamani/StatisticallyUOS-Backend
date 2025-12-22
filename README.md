Tech:
Backend: FastAPI
Database: PostgreSQL (via SQLAlchemy ORM)
Scraper: BeautifulSoup4 & Subprocess (Curl)
Data Validation: Pydantic v2
Environment: Python 3.10+

How to set it up:
# Clone the repository
git clone <your-repo-link>
cd project_usindh

# Create and activate virtual environment
python -m venv venv
./venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt


Project folder structure:
project_usindh/
├── src/
│   ├── config/       # Database connection & Base
│   ├── db_models/    # SQLAlchemy models
│   ├── models/       # Pydantic schemas
│   ├── scraper/      # BeautifulSoup logic & HTML files
│   └── seed/         # Scripts to populate the DB
├── .env              # Secrets (ignored by git)
├── main.py           # FastAPI Entry point
└── requirements.txt

To Scrape & Seed the Database run:
Bash
python -m src.seed.insert_departments

