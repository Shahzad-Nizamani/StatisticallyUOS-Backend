from bs4 import BeautifulSoup

def parsed_course(html):
    soup = BeautifulSoup(html, "html.parser")

    courses = []

    try:
        result_table = soup.find_all("table")[1]
        result_rows = result_table.find_all("tr")

        for i in range(1, len(result_rows)):
            course = {}

            if result_rows[i].find_all("td"):
            
                cells = result_rows[i].find_all("td")
                course_code = cells[0].text.strip()
                course_name = cells[1].text.strip()

                course["course_code"] = course_code
                course["course_name"] = course_name
                
                courses.append(course) 
    
    except Exception as e:
        print(f"Error parsing course: {e}")
        
    return courses