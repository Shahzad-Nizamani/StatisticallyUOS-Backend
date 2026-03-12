from fastapi.requests import Request
from sqlalchemy import text
from src.config.db_config import session
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

    matched_files = list(BASE_DIR.glob(f"*_{dept_id}.jpg"))
    name_words = [w.lower() for w in name.split() if len(w) > 2]
    best_match, best_score = None, 0

    for f in matched_files:
        score = sum(1 for word in name_words if word in f.name.lower())
        if score > best_score:
            best_score = score
            best_match = f

    teacher_dict["photo_url"] = (
        str(request.url_for("get_teacher_image", filename=best_match.name))
        if best_match and best_score > 0 else None
    )
    return teacher_dict


def fetch_teachers_by_dept(dept_id: int, request: Request):
    db_session = session()
    teachers = db_session.execute(
        text("SELECT tid, name, role, dept_id FROM teacher WHERE dept_id = :dept_id"),
        {"dept_id": dept_id}
    ).fetchall()
    db_session.close()

    if not teachers:
        return {"teachers": []}

    dept_files = list(BASE_DIR.glob(f"*_{dept_id}.webp"))

    def find_photo(name):
        name_words = [w.lower() for w in name.split() if len(w) > 2]
        best_match, best_score = None, 0
        for f in dept_files:
            score = sum(1 for word in name_words if word in f.name.lower())
            if score > best_score:
                best_score = score
                best_match = f
        return (
            str(request.url_for("get_teacher_image", filename=best_match.name))
            if best_match and best_score > 0 else None
        )

    return {
        "teachers": [
            {**dict(row._mapping), "photo_url": find_photo(row.name)}
            for row in teachers
        ]
    }