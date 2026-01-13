from bs4 import BeautifulSoup

def parsed_student(html):

    html = html
    soup = BeautifulSoup(html, 'html.parser')

    student = {}

    try:
        tables = soup.find_all('table')
        st_info = tables[0].find_all("b")

        roll_no = st_info[3].text
        student["roll_no"] = roll_no

        name = st_info[0].text
        student["name"] = name

        fname = st_info[1].text
        student["fname"] = fname

        surname = st_info[2].text
        student["surname"] = surname

        result = tables[2].find_all("b")

        cgpa = result[1].text
        if cgpa == "---":
           student["cgpa"] = None
        else: student["cgpa"] = cgpa 

        if cgpa == "---":
           student["cgpa"] = None
        else: student["cgpa"] = cgpa 

        percentage = result[3].text
        if percentage == "---":
           student["percentage"] = None
        else: student["percentage"] = percentage 

    
    except Exception as e:
        print(f"Error parsing student: {e}")

    return student