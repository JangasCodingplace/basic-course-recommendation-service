from fastapi import FastAPI
from .repositories import UserRepository, RecommendationRepository
from .models import CourseEssential
from .configs import EXEC_INITIAL_LOAD
from .initial_load import exec_initial_load


if EXEC_INITIAL_LOAD:
    exec_initial_load()


app = FastAPI()


@app.get("/course-recommendation/{user_id}")
def get_recommendation(user_id: int) -> list[CourseEssential]:
    return RecommendationRepository.get_course_recommendation_by_use_case(user_id=user_id)


@app.get("/courses-by-user/{user_id}")
def get_courses_by_user(user_id: int) -> list[CourseEssential]:
    return UserRepository.get_courses(id_=user_id)
