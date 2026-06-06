import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
from src.seed.insert_all import insert_all_to_db
from src.scraper.parse_student import parsed_student
from src.scraper.parse_course import parsed_course
from src.scraper.parse_result import parsed_result

def scrape_all():
    req_session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    req_session.mount('https://', adapter)

    url = "https://exam.usindh.edu.pk/v2/transcript_handler.php"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://exam.usindh.edu.pk/v2/trancript.php",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://exam.usindh.edu.pk",
        "Connection": "keep-alive",
        "X-Requested-With": "XMLHttpRequest"
    }

    with open("src/scraper/rollno_codes.json", 'r') as f:
        codes = json.load(f)

    depts = codes

    try:
        for dept_id in depts:
            print(f"\n{'='*60}")
            print(f"PROCESSING DEPARTMENT WITH ID: {dept_id}")
            print(f"{'='*60}")

            year = 22
            seen_courses = set()

            while year <= 25:
                students_list = []
                results_list = []
                courses_list = []

                print(f"\n--- Processing Year: 2K{year:02d} ---")
                n = 1
                consecutive_not_found = 0
                students_found_this_year = 0

                payload_year = 2025
                part = payload_year - (year + 2000) + 1
                exam_year = payload_year
                print("PART---- ", part)

                while consecutive_not_found < 10:
                    student_found = False
                    student = None  # ← reset explicitly every iteration

                    try:
                        rollno = f"2K{year}/{depts[dept_id]}/{n}"
                        payload = {
                            "roll_no": rollno,
                            "exam_year": exam_year,
                            "part": part
                        }

                        print(f"Fetching: {rollno}, Part {part}...", end=" ")
                        response = req_session.post(url, headers=headers, data=payload, timeout=30)
                        print(f"Status: {response.status_code}")

                        soup = BeautifulSoup(response.text, "html.parser")
                        tables = soup.find_all("table")
                        print(f"  Tables found: {len(tables)}")

                        if len(tables) != 3:
                            print(f"  ✗ Student not found")
                            consecutive_not_found += 1
                            print(f"  Consecutive not found: {consecutive_not_found}/10")
                            n += 1
                            continue

                        html = response.text
                        student_found = True

                        student = parsed_student(html)
                        courses = parsed_course(html)
                        student_results = parsed_result(html)

                        if student:
                            for course in courses:
                                key = (course["course_code"], course["course_name"])
                                if key not in seen_courses:
                                    courses_list.append(course)
                                    seen_courses.add(key)
                                print(course)

                            for result in student_results:
                                result["roll_no"] = rollno
                                result["year"] = exam_year
                                results_list.append(result)
                                print(result)

                            print(f"  ✓ Student data parsed")
                        else:
                            print(f"  ⚠ Parsing failed")
                            student_found = False  # parsing failed, treat as not found

                    except requests.exceptions.RequestException as e:
                        print(f"  ✗ Request failed: {e}")

                    except Exception as e:
                        print(f"  ✗ Error processing: {e}")

                    # Update consecutive not found counter
                    if student_found:
                        consecutive_not_found = 0
                    else:
                        consecutive_not_found += 1
                        print(f"  Consecutive not found: {consecutive_not_found}/10")

                    if student_found and student:
                        student["dept_id"] = dept_id
                        print(f"Final student: {student}")
                        students_list.append(student)
                        students_found_this_year += 1

                    time.sleep(3)
                    n += 1  # ← always increments, never skipped

                if students_list:
                    insert_all_to_db(students_list, courses_list, results_list)
                    print(f"\nYear 2K{year:02d} complete: Found {students_found_this_year} students")
                else:
                    print(f"\nNo students found in year 2K{year:02d}")

                year += 1

            print(f"\n{'='*60}")
            print(f"Finished Department id {dept_id}!")

        print(f"\n{'='*60}")
        print(f"SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"✓ Successfully saved records to DB.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    scrape_all()