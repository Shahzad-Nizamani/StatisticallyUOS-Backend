Tech:FastAPI


Database: PostgreSQL (via SQLAlchemy ORM)
Scraper: Requests and BeautifulSoup4
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

Step 1:
Create a .env file with 
database_url = postgresql://postgres:xnfooty1@localhost:5432/project_usindh
in it.

Step 2: To Scrape & Seed the Database run:
python -m src.seed.seed_dept


Project folder structure:
project_usindh/
├── src/
│   ├── config/       # Database connection & Base
│   ├── db_models/    # SQLAlchemy models
│   ├── scraper/      # BeautifulSoup logic & HTML files
│   └── seed/         # Scripts to populate the DB
├── .env              # Secrets (ignored by git)
├── main.py           # FastAPI Entry point
└── requirements.txt


To Scrape & Seed the Database run:
scrap_and_seed_all.py

