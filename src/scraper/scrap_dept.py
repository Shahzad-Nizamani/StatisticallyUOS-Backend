from selenium import webdriver
import json 
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

driver.get("https://exam.usindh.edu.pk/v2/course.php")
soup = BeautifulSoup(driver.page_source, "html.parser")

departments = {}

dept = soup.find_all('select')[1].find_all('option')
for i in range(1,len(dept)):

    did = f'D{i}'
    departments[did] = dept[i].text.strip()

with open("src\scraper\departments.json", 'w') as f:
    json.dump(departments, f, indent=4)

driver.quit()
