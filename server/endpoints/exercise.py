from typing import List, Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from models import Workout, Exercise
from schemas import ExerciseCreateSchema, ExerciseUpdateSchema, ExerciseOutSchema
from deps import get_db, get_current_workout, get_current_exercise

router = APIRouter()

@router.get("/workouts/{workout_id}/exercises", response_model=List[ExerciseOutSchema])
async def get_exercises(
    workout_id: int,
    current_workout: Annotated[Workout, Depends(get_current_workout)]
    ):

    return current_workout.exercises

@router.post("/workouts/{workout_id}/exercises", response_model=ExerciseOutSchema)
async def create_exercise(
    workout_id: int,
    exercise_in: ExerciseCreateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_workout: Annotated[Workout, Depends(get_current_workout)]
    ):

    exercise = Exercise(name=exercise_in.name)
    current_workout.exercises.append(exercise)
    db.commit()

    return exercise 

@router.get("/workouts/{workout_id}/exercises/{exercise_id}", response_model=ExerciseOutSchema)
async def get_exercise(
    exercise_id: int,
    workout_id: int,
    current_exercise: Annotated[Exercise, Depends(get_current_exercise)]
    ):

    return current_exercise

@router.patch("/workouts/{workout_id}/exercices/{exercise_id}", response_model=ExerciseOutSchema)
async def update_exercise(
    exercise_id: int,
    workout_id: int,
    exercise: ExerciseUpdateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_exercise: Annotated[Exercise, Depends(get_current_exercise)]
    ):

    for var, value in vars(exercise).items():
        setattr(current_exercise, var, value) if value else None
    db.commit()

    return current_exercise

@router.delete("/workouts/{workout_id}/exercises/{exercise_id}", response_model=ExerciseOutSchema)
async def remove_exercise(
    exercise_id: int,
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_exercise: Annotated[Exercise, Depends(get_current_exercise)]
    ):

    db.delete(current_exercise)
    db.commit()

    return current_exercise