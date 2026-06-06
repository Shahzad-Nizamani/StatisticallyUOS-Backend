from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.cgpa_leaderboard import router as cgpa_router
from src.routes.subject_overview import router as subject_router
from src.routes.load_courses import router as load_courses_router
from src.routes.teacher_routes import router as teacher_router
from src.routes.all_time_subject_leaderboard import router as all_time_subject_leaderboard_router
from src.routes.batch_wise_subject_laederboard import router as batch_wise_subject_laederboard_router
from src.routes.photos import router as photos_router
from src.routes.students_routes import router as students_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cgpa_router)
app.include_router(subject_router)
app.include_router(all_time_subject_leaderboard_router)
app.include_router(batch_wise_subject_laederboard_router)
app.include_router(load_courses_router)
app.include_router(teacher_router)
app.include_router(photos_router)
app.include_router(students_router)