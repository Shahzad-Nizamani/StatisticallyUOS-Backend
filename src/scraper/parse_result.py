from bs4 import BeautifulSoup

def parsed_result(html):
    soup = BeautifulSoup(html, "html.parser")

    results = []

    try:
        tables = soup.find_all('table')
        result_table = tables[1]
        result_rows = result_table.find_all("tr")
        
        student_table = tables[0]  
        st_info = student_table.find_all("b")

        roll_no = st_info[3].text

        for i in range(1, len(result_rows)):
            result = {}
            result["roll_no"] = roll_no
            
            cells = result_rows[i].find_all("td")

            if cells:
                course_code = cells[0].text.strip()
                marks = cells[4].text.strip()
                grade = cells[5].text.strip()

                result["course_code"] = course_code
                
                if marks == "AB#":
                    marks = None
                else: result["marks"] = marks
                result["grade"] = grade
                
                results.append(result) 
    
    except Exception as e:
        print(f"Error parsing course: {e}")
            
    return results