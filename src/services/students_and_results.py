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