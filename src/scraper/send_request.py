import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
from parse_student import parsed_student
import json

def send_req():
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

    year = 24
    depts = ["CSM", "CSE"]
    students = []

    try:
        for dept in depts:
            print(f"\n=== Processing Department: {dept} ===")
            n = 1
            consecutive_not_found = 0
            
            while consecutive_not_found < 5:
                student_found = False
                
                try:
                    part = 1
                    results = True
                    
                    while results:
                        rollno = f"2K{year}/{dept}/{n}"
                        payload = {
                            "roll_no": rollno,
                            "exam_year": 2024,
                            "part": part
                        }
                        
                        print(f"Fetching: {rollno}, Part {part}...", end=" ")
                        response = session.post(url, headers=headers, data=payload, timeout=30)
                        print(f"Status: {response.status_code}")
                        
                        soup = BeautifulSoup(response.text, "html.parser")
                        tables = soup.find_all("table")
                        print(f"{len(tables)} found!")
                        
                        # Check if student exists (at least 2 tables expected)
                        if len(tables) >= 2:
                            student_found = True
                            student = parsed_student(response.text)
                            
                            # Only append if parsing returned valid data
                            if student:
                                students.append(student)
                                print(f"  ✓ Student data saved")
                            else:
                                print(f"  ⚠ Parsing failed")
                        else:
                            print(f"  ✗ Student not found")
                        
                        # Check if results for this part exist (3 tables = results available)
                        if len(tables) != 3:
                            results = False
                        
                        part += 1
                        time.sleep(3)  # Rate limiting
                    
                    # Update consecutive counter based on whether student was found
                    if student_found:
                        consecutive_not_found = 0
                    else:
                        consecutive_not_found += 1
                        print(f"  Consecutive not found: {consecutive_not_found}/5")
                
                except requests.exceptions.RequestException as e:
                    print(f"  ✗ Request failed for {rollno}: {e}")
                    consecutive_not_found += 1
                except Exception as e:
                    print(f"  ✗ Error processing {rollno}: {e}")
                    consecutive_not_found += 1
                
                n += 1
            
            print(f"Finished {dept}: Found {sum(1 for s in students if s.get('dept') == dept)} students")
        
        # Save results
        output_file = "students.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(students, f, indent=4, ensure_ascii=False)
        
        print(f"\n✓ Successfully saved {len(students)} student records to {output_file}")
        return students

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    send_req()