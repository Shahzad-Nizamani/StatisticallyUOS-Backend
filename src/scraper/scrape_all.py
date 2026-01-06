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

from scraper.parse_student import parsed_student
from scraper.parse_course import parsed_course
from scraper.parse_result import parsed_result
from scraper.dept_names_and_codes import get_dept_codes

import json

def scrape_all():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

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

    depts = get_dept_codes()
    
    students = []

    try:
        for dept_name in depts:
            print(f"\n{'='*60}")
            print(f"PROCESSING DEPARTMENT: {dept_name}")
            print(f"{'='*60}")
            
            year = 4
            
            while year <= 24:
                print(f"\n--- Processing Year: 2K{year:02d} ---")
                n = 1
                consecutive_not_found = 0
                students_found_this_year = 0
                
                # Process students in this year
                while consecutive_not_found < 5:
                    student_found = False
                    
                    try:
                        part = 1
                        results = True
                        payload_year = year
                        
                        # Process all parts for this roll number
                        while results:
                            exam_year = f"20{payload_year:02d}"
                            
                            rollno = f"2K{year}/{depts[dept_name]}/{n}"
                            payload = {
                                "roll_no": rollno,
                                "exam_year": exam_year,
                                "part": part
                            }
                            
                            print(f"Fetching: {rollno}, Part {part}...", end=" ")
                            response = session.post(url, headers=headers, data=payload, timeout=30)
                            print(f"Status: {response.status_code}")
                            
                            soup = BeautifulSoup(response.text, "html.parser")
                            tables = soup.find_all("table")
                            print(f"  Tables found: {len(tables)}")
                            
                            # Check if results for this part exist (3 tables = results available)
                            if len(tables) != 3:
                                print(f"  No more parts for this student")
                                results = False

                            # Check if student exists (at least 2 tables expected)
                            if len(tables) >= 2:
                                html = response.text
                                student_found = True

                                student = parsed_student(html)
                                student["dept_name"] = dept_name
                                print(student)

                                courses = parsed_course(html)
                                for course in courses:
                                    course["dept_name"] = dept_name
                                    print(course)

                                student_results = parsed_result(html)
                                for result in student_results:
                                    result["roll_no"] = rollno
                                    print(result)
                                                              
                                # Only append if parsing returned valid data
                                if student:
                                    students.append(student)
                                    students_found_this_year += 1
                                    print(f"  ✓ Student data saved")
                                else:
                                    print(f"  ⚠ Parsing failed")
                            else:
                                print(f"  ✗ Student not found")
                            
                            part += 1
                            payload_year += 1
                            time.sleep(3)  # Rate limiting
                        
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
                         
                    n += 1
                
                print(f"\nYear 2K{year:02d} complete: Found {students_found_this_year} students")
                
                # Move to next year
                year += 1
            
            print(f"\n{'='*60}")
            print(f"Finished {dept_name}!")
        
        output_file = "students.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(students, f, indent=4, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"✓ Successfully saved {len(students)} student records to {output_file}")
        return students

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    scrape_all()