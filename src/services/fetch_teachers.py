from sqlalchemy import text
from src.config.db_config import session
from fastapi.requests import Request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "teachers"

def get_teacher_by_tid(tid, request: Request):
    db_session = session()
    teacher = db_session.execute(
        text("SELECT tid, name, role, dept_id FROM TEACHER WHERE tid = :tid"), {"tid": tid}
    ).fetchone()
    db_session.close()

    if teacher is None:
        return None

    teacher_dict = dict(teacher._mapping)

    dept_id = teacher_dict.get("dept_id")
    name = teacher_dict.get("name")

    # Get all files for this dept
    matched_files = list(BASE_DIR.glob(f"*_{dept_id}.jpg"))

    # Score each file by how many words from the teacher's name appear in the filename
    name_words = [w.lower() for w in name.split() if len(w) > 2]  # skip short words like MS, DR
    
    best_match = None
    best_score = 0

    for f in matched_files:
        fname_lower = f.name.lower()
        score = sum(1 for word in name_words if word in fname_lower)
        if score > best_score:
            best_score = score
            best_match = f

    if best_match and best_score > 0:
        teacher_dict["photo_url"] = str(request.url_for("get_teacher_image", filename=best_match.name))
    else:
        teacher_dict["photo_url"] = None

    return teacher_dict

def fetch_teachers(request: Request):
    db_session = session()
    result = db_session.execute(text("SELECT tid, name, role, dept_id FROM teacher"))
    teachers = result.fetchall()
    db_session.close()

    # Load all files once grouped by dept_id
    all_files = list(BASE_DIR.glob("*.jpg"))
    files_by_dept = {}
    for f in all_files:
        # extract dept_id from filename: _{name}_{dept_id}.jpg
        try:
            dept_id = int(f.stem.split("_")[-1])
            files_by_dept.setdefault(dept_id, []).append(f)
        except ValueError:
            continue

    def find_photo(name, dept_id):
        candidates = files_by_dept.get(dept_id, [])
        name_words = [w.lower() for w in name.split() if len(w) > 2]
        best_match, best_score = None, 0
        for f in candidates:
            score = sum(1 for word in name_words if word in f.name.lower())
            if score > best_score:
                best_score = score
                best_match = f
        return str(request.url_for("get_teacher_image", filename=best_match.name)) if best_match and best_score > 0 else None

    return {
        "teachers": [
            {**dict(row._mapping), "photo_url": find_photo(row.name, row.dept_id)}
            for row in teachers
        ]
    }