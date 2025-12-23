import json
import subprocess
import sys
from bs4 import BeautifulSoup
from src.models.department import department

# Function to download the HTML using curl or wget
def download_html(url, output_file):
    try:
        # Try curl first
        subprocess.run(["curl", "-L", "-o", output_file, url], check=True)
    except FileNotFoundError:
        # If curl is not available, try wget
        try:
            subprocess.run(["wget", "-O", output_file, url], check=True)
        except FileNotFoundError:
            print("Error: Neither curl nor wget is installed.")
            sys.exit(1)

# URL to download
url = "https://exam.usindh.edu.pk/v2/course.php"
html_file = "src/scraper/departments.html"

def get_departments():

        # Download HTML
    download_html(url, html_file)
    # Read the downloaded HTML
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Find the select element for departments
    select = soup.find("select", {"name": "dept_id"})
    if not select:
        print("Error: Could not find the department select element.")
        sys.exit(1)

    departments = []
    id_counter = 1

    for option in select.find_all("option"):

        Did = option.get("value")
        name = option.text.strip()

        if Did and Did.isdigit():
            Did = int(Did)
            dic = {
                   "id" : id_counter,
                    "Did": Did, 
                    "name": name
                    }
            departments.append(dic)

            id_counter += 1

    print("Scraped all departments succesfully.")

    return departments