import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import json
import time
from parse_teacher import parse_teacher
from src.seed.insert_teacher import insert_teacher_to_db

def scrap_teachers():
    req_session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    req_session.mount('https://', adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://usindh.edu.pk/",
        "Connection": "keep-alive",
    }

    # with open("src/scraper/rollno_codes.json", 'r') as f:
     #    depts = json.load(f)

    depts = [263, 300, 292, 235, 49, 2, 78, 255, 82, 215, 241, 239, 254, 11, 238, 67, 74, 236, 250, 15, 45, 301, 249, 20, 31, 286, 285, 218, 284, 92, 8, 6, 124, 43, 59, 17, 275, 291, 7, 70, 28, 3, 44, 81, 62, 69, 68, 172, 225, 80, 93, 123, 247, 224, 193, 200, 94, 86, 51, 233, 229, 231, 230, 63, 232, 281, 258, 115, 75, 240, 305, 237, 79, 283, 116, 88, 306, 76, 302, 289, 309, 213, 210, 308, 290, 216, 208, 16, 87, 85, 77, 13, 83, 89, 14, 253, 71, 500, 217, 214, 287, 211, 288, 303]
    
    total_teachers = 0
    os.makedirs('static/images/teachers', exist_ok=True)
    
    for dept_id in depts:
        dept_teachers_list = []

        print(f"\n{'='*60}")
        print(f"Processing dept {dept_id}")
        print(f"{'='*60}")
        
        url = f"https://usindh.edu.pk/faculty_members/{dept_id}"

        try:
            html = req_session.get(url, headers=headers, timeout=10).text
            soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            print(f"✗ Error fetching dept {dept_id}: {e}")
            continue
        
        cards = soup.find_all("div", "card border-1")
        if not cards:
            print(f"⚠️  No teachers found for dept {dept_id}")
            continue
        
        print(f"Found {len(cards)} teachers")
        
        for card in cards:
            teacher = parse_teacher(card)
            name = teacher["name"]
            original_url = teacher["original_image_url"]
            
            print(f"\n{name}")
            
            image_path = None
            try:
                print(f"Downloading: {original_url}")
                img_data = req_session.get(original_url, headers=headers, timeout=15)
                print(f"Status: {img_data.status_code}, Size: {len(img_data.content)} bytes")
                
                if img_data.status_code == 200 and len(img_data.content) > 0:
                    file_name = "".join(c if c.isalnum() or c == ' ' else '_' for c in name)
                    file_name = file_name.replace(' ', '_') + '_' + str(dept_id) + '.jpg'
                    
                    filepath = f'static/images/teachers/{file_name}'
                    with open(filepath, 'wb') as f:
                        f.write(img_data.content)
                    
                    image_path = f'images/teachers/{file_name}'
                    print(f"✓ Saved: {filepath}")
                else:
                    image_path = 'images/teachers/default-avatar.png'
                    print(f"✗ Failed download")
                    
            except Exception as e:
                image_path = 'images/teachers/default-avatar.png'
                print(f"✗ Error: {e}")
            
            teacher_data = {
                "name": name,
                "role": teacher["role"],
                "image_path": image_path,
                "original_image_url": original_url,
                "dept_id": int(dept_id)
            }
            dept_teachers_list.append(teacher_data)
        
        if dept_teachers_list:
            try:
                insert_teacher_to_db(dept_teachers_list)
                total_teachers += len(dept_teachers_list)
                print(f"✓ Inserted {len(dept_teachers_list)} teachers from dept {dept_id}")
            except Exception as e:
                print(f"✗ Failed to insert: {e}")
        
        time.sleep(3)
    
    print(f"\n{'='*60}")
    print(f"✓ Scraping complete! Total: {total_teachers} teachers")
    print(f"{'='*60}")

if __name__ == '__main__':
    scrap_teachers()