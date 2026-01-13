import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.scraper.scrape_all import scrape_all
from create_tables import create_tables
from seed_dept import seed_dept

def seed_all():
    create_tables()
    seed_dept()

    try:
        scrape_all()
    except KeyboardInterrupt as e:
        print("Scraping stopped by the user!")


if __name__ =="__main__":
    seed_all()