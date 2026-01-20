import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
from scraper.parse_student import parsed_student
from scraper.parse_course import parsed_course
from scraper.parse_result import parsed_result
from seed.insert_all import insert_all_to_db
from scraper.dept_names_and_codes import get_dept_codes
import datetime

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

   # with open("src/scraper/rollno_codes.json", 'r') as f:
    #    codes = json.load(f)

    depts = {10: "CSM"}

    try:
        for dept_id in depts:
            print(f"\n{'='*60}")
            print(f"PROCESSING DEPARTMENT WITH ID: {dept_id}")
            print(f"{'='*60}")
            
            year = 24
            seen_courses = set()

            while year <= 24:
                students_list = []
                results_list = []
                courses_list = []

                print(f"\n--- Processing Year: 2K{year:02d} ---")
                n = 150
                consecutive_not_found = 0
                students_found_this_year = 0
                
                # Process students in this year
                while consecutive_not_found < 8:
                    student_found = False
                    
                    try:
                        part = 1
                        results = True
                        payload_year = year
                        
                        # Process all parts for this roll number
                        while results:
                            exam_year = f"20{payload_year:02d}"
                            
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
                            
                            # Check if results for this part exist (3 tables = results available)
                            if len(tables) != 3:
                                print(f"  No more parts for this student")
                                results = False
                                continue

                            # Check if student exists (at least 2 tables expected)
                            if len(tables) >= 2:
                                html = response.text
                                student_found = True

                                student = parsed_student(html)
                                courses = parsed_course(html)
                                student_results = parsed_result(html)
                                                              
                                # Only append if parsing returned valid data
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

                                    print(f"  ✓ Student data saved")
                                else:
                                    print(f"  ⚠ Parsing failed")
                            else:
                                print(f"  ✗ Student not found")
                            
                            part += 1
                            payload_year += 1
                            time.sleep(2)  # Rate limiting
                        
                        # Update consecutive not found counter
                        if student_found:
                            consecutive_not_found = 0
                        else:
                            consecutive_not_found += 1
                            print(f"  Consecutive not found: {consecutive_not_found}/5")
                        
                    except requests.exceptions.RequestException as e:
                        print(f"  ✗ Request failed: {e}")
                        
                    except Exception as e:
                        print(f"  ✗ Error processing: {e}")  
                    
                    if student_found and student:
                        student["dept_id"] = dept_id
                        print(f"Final student: {student}")
                        students_list.append(student)
                        students_found_this_year += 1 

                    n += 1
                
                if students_list:
                   insert_all_to_db(students_list, courses_list, results_list)
                   print(f"\nYear 2K{year:02d} complete: Found {students_found_this_year} students")
                else:
                    print(f"\nNo students found in year 2K{year:02d}")
                
                # Move to next year
                year += 1
            
            print(f"\n{'='*60}")
            print(f"Finished {dept_id}!")
        
        print(f"\n{'='*60}")
        print(f"SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"✓ Successfully saved records to DB.")

    except Exception as e:
        print(f"\n Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    scrape_all()