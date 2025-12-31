from bs4 import BeautifulSoup

def parsed_student(html):

    html = html
    soup = BeautifulSoup(html, 'html.parser')

    student = {}

    tables = soup.find_all('table')
    st_info = tables[0].find_all("b")

    roll_no = st_info[3].text
    student["roll_no"] = roll_no

    name = st_info[0].text
    student["name"] = name

    fname = st_info[1].text
    student["fname"] = fname

    sruname = st_info[2].text
    student["sruname"] = sruname

    result = tables[2].find_all("b")

    cgpa = result[1].text
    student["cgpa"] = cgpa

    percentage = result[3].text
    student["percentage"] = percentage

    return student