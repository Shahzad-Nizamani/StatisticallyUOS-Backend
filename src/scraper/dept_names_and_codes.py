import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
from bs4 import BeautifulSoup
from sqlalchemy import select
from config.db_config import session as db_session_factory
from src.db_models.department import Department
from src.db_models.course import Course
from src.db_models.student import Student
from src.db_models.result import Result
import time
import json

def load_departments_from_db():
    db_session = db_session_factory()
    try:
        query = select(Department.did, Department.dname)
        depts = db_session.execute(query).mappings().all()
    finally:
        db_session.close()
    
    return depts

def get_dept_codes():
    depts = load_departments_from_db()
    depts_and_rollno_codes = {
            2 : "BBA",
            10: "CSM",
            501 : "CSE"
        }
    
    req_session = requests.Session()

    program_api = "https://exam.usindh.edu.pk/v2/getProgram.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://exam.usindh.edu.pk/v2/trancript.php",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }

    req_session.get("https://exam.usindh.edu.pk/v2/trancript.php", headers=headers)

    for dept in depts:
        dept_id = dept["did"]
        dept_name = dept["dname"]

        print(f"\n Processing Department: {dept_name}....")
        prog_id = None
        batch = None

        params = {
            "depId": dept_id
        }
        
        try:
            program_response = req_session.get(program_api, headers=headers, params=params)
            print("Status Code:", program_response.status_code)
            print(program_response.text)

            soup = BeautifulSoup(program_response.text, "html.parser")

            find_BS = soup.find("option", string=lambda text: "BS" in text if text else False)

            if find_BS:
                prog_id = find_BS['value']
                params["progId"] = prog_id
                print(f"Found program ID: {prog_id}")
            else:
                print(f"No program with 'BS' found for department {dept_name}. Skipping...")
                continue
                
        except Exception as e:
            print(f"An error occurred while finding PROGRAM_ID for department {dept_name}: {e}")
            continue

        if prog_id is None:
            print(f"Skipping department {dept_name} - no valid program ID")
            continue

        payload = {
        "semester" : "1",
        "exam_year" : "2024",
    }
        try:
            batch_payload = {
                "dept_id": dept_id,
                "program_id": prog_id,
                "semester": "1",
                "exam_year": "2024"
            }
            batch_api = "https://exam.usindh.edu.pk/v2/getBatch.php"
            batch_response = req_session.get(batch_api, headers=headers, params=batch_payload)
            soup = BeautifulSoup(batch_response.text, "html.parser")

            find_regular = soup.find("option", string=lambda text: "REGULAR" in text if text else False)
            if find_regular:
                batch = find_regular["value"].split("~")[0]
                print(f"Found batch: {batch}")
                payload["batch"] = batch
            else:
                print(f"No REGULAR batch found for department {dept_name}")
                
        except Exception as e:
            print(f"An error occurred while finding BATCH for department {dept_name}: {e}")

        courses_api = "https://exam.usindh.edu.pk/v2/getCources.php"
        course_payload = {
            "depId": dept_id,
            "progId": prog_id,
            "semester": "1",
            "year": "2024",
            "groupDesc" : "GNRL"
        }

        try:
            course_response = req_session.get(courses_api, headers=headers, params=course_payload)
            soup = BeautifulSoup(course_response.text, "html.parser")

            course_option = soup.find("option")
            if course_option and "value" in course_option.attrs:
                course_code = course_option["value"]
                print(f"Course code: {course_code}")
                payload["courseNo"] = course_code
            else:
                print(f"No course found for department {dept_name}")
            
        except Exception as e:
            print(f"An error occurred while finding COURSE for department {dept_name}: {e}")
        
        try:
            subwise_result_api = "https://exam.usindh.edu.pk/v2/course_summary.php"
            resp = req_session.get(subwise_result_api, headers=headers, params=payload)
            soup = BeautifulSoup(resp.text, "html.parser")
            
            res_table = soup.find("table")

            rollno = res_table.find_all("th")[2].text
            rollno_code = rollno.split("/")[1].split("/")[0]
            if rollno_code:
                depts_and_rollno_codes[dept_id] = rollno_code
                print(f"{dept_name} : {rollno_code}")

        except Exception as e:
            print(f"An error occurred while getting rollno for department {dept_name}: {e}")

        time.sleep(2)
    
    with open("src/scraper/rollno_codes.json", 'w') as f:
        json.dump(depts_and_rollno_codes, f, indent=4)

    return depts_and_rollno_codes

if __name__ == '__main__':
    get_dept_codes()