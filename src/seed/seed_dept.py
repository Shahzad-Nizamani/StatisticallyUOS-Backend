import os
from src.scraper.scrap_dept import get_departments, html_file
from src.seed.insert_departments import save_dept_toDB

def seed_dept():
    scaped_departments = get_departments()
    save_dept_toDB(scaped_departments)

    if os.path.exists(html_file):
        os.remove(html_file)
        print(f"{html_file} has been deleted.")
    else:
        print("The file does not exist.")

if __name__ == "__main__":
    seed_dept()