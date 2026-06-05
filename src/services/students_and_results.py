from src.config.db_config import session
from sqlalchemy import text
from rapidfuzz import fuzz

def fetch_students(name: str = None, surname: str = None, dept_id: int = None, batch: str = None):
    db_session = session()
    
    # Build WHERE clause dynamically
    where_conditions = []
    params = {}
    
    # Stage 1: Database filter with prefix + Levenshtein distance (word boundary OR typo tolerance)
    if name:
        where_conditions.append("(s.name ~* :name_pattern OR levenshtein(LOWER(s.name), LOWER(:name)) <= 1)")
        params["name_pattern"] = f"\\y{name.upper()}"
        params["name"] = name.lower()
    
    if surname:
        where_conditions.append("(s.surname ~* :surname_pattern OR levenshtein(LOWER(s.surname), LOWER(:surname)) <= 1)")
        params["surname_pattern"] = f"\\y{surname.upper()}"
        params["surname"] = surname.lower()
    
    if dept_id:
        where_conditions.append("s.dept_id = :dept_id")
        params["dept_id"] = dept_id
    
    if batch:
        where_conditions.append("s.roll_no like :batch")
        params["batch"] = f"{batch}%"
    
    # Construct query
    base_query = "SELECT s.roll_no, s.name, s.fname, s.surname, d.dname FROM student s JOIN department d ON s.dept_id = d.did"
    
    if where_conditions:
        base_query += " WHERE " + " AND ".join(where_conditions)
    
    results = db_session.execute(text(base_query), params).fetchall()
    db_session.close()
    
    # Stage 2: Python-side fuzzy refinement (partial matching for additional filtering)
    if name and results:
        results = [
            row for row in results
            if fuzz.partial_ratio(name.upper(), row.name.upper()) >= 80
        ]
    
    if surname and results:
        results = [
            row for row in results
            if fuzz.partial_ratio(surname.upper(), row.surname.upper()) >= 80
        ]
    
    return results

def fetch_results_by_roll_no(roll_no: str):
    db_session = session()
    
    result_query = text("SELECT r.*, c.course_name FROM result r JOIN course c ON r.course_code = c.course_code WHERE r.roll_no = :roll_no")
    results = db_session.execute(result_query, {"roll_no": roll_no}).fetchall()
    
    student_query = text("SELECT * FROM student WHERE roll_no = :roll_no")
    student = db_session.execute(student_query, {"roll_no": roll_no}).fetchone()
    
    db_session.close()
    
    student = dict(db_session.execute(student_query, {"roll_no": roll_no}).fetchone()._mapping)

    student_dict = {
        "name": student["name"],
        "fname": student["fname"],
        "surname": student["surname"],
        "cgpa": student["cgpa"],
        "percentage": student["percentage"]
    }
    
    serialized = [dict(row._mapping) for row in results]
    
    batch_year = 2000 + int(roll_no.split("/")[0][2:])  # "2K24" -> 2024
    
    parts = {}
    for row in serialized:
        part = row["year"] - batch_year + 1
        key = f"part {part}"
        if key not in parts:
            parts[key] = []
        parts[key].append({
            "roll_no": row["roll_no"],
            "course_code": row["course_code"],
            "marks": row["marks"],
            "grade": row["grade"],
            "course_name": row["course_name"]
        })
    
    return {
        "student": student_dict,
        "results": parts
    }