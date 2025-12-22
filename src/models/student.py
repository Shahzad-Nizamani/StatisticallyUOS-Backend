from pydantic import BaseModel

class Student(BaseModel):
    rollno : str
    name : str
    fname : str
    surname : str
    gender : str
    cgpa : float
    percentage : float