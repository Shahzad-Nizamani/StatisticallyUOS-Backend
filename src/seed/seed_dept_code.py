from src.config.db_config import session
import json
from sqlalchemy import text

with open(r"src\scraper\progress.json", 'r') as f:
    data = json.load(f)

db_session = session()

for dept_id in data:
    db_session.execute(
        text("UPDATE department SET dept_code = :dept_code WHERE did = :dept_id"),
        {"dept_code": data[dept_id], "dept_id": dept_id}
    )

db_session.commit()
db_session.close()