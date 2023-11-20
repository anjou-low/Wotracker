from fastapi import APIRouter
from endpoints import user, workout, exercise, set

api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(workout.router)
api_router.include_router(exercise.router)
api_router.include_router(set.router)