# students_routes.py
from fastapi import APIRouter
from typing import Optional
from src.services.students_and_results import fetch_students

app = APIRouter()

@app.get("/students")
def get_students(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    dept_id: Optional[int] = None,
    batch: Optional[str] = None
):
    # At least one parameter should be provided (validate on frontend)
    results = fetch_students(name=name, surname=surname, dept_id=dept_id, batch=batch)
    
    return {
        "count": len(results),
        "students": [
            {
                "roll_no": r[0],
                "name": r[1],
                "fname": r[2],
                "surname": r[3],
                "department": r[4]
            }
            for r in results
        ]
    }