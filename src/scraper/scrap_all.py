from send_request import send_req
from parse_student import parsed_student

def parse_result():

    html = send_req()
    student = parsed_student(html)
    
parse_result()