from datetime import datetime
from typing import List, Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from models import User, Workout, Exercise, Set
from schemas import WorkoutCreateSchema, WorkoutUpdateSchema, WorkoutOutSchema
from deps import get_db, get_current_user, get_current_workout

router = APIRouter()

@router.get("/workouts", response_model=List[WorkoutOutSchema])
async def get_workouts(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
    ):

    workouts = db.query(Workout).filter(Workout.user_id == current_user.id).all()
    return workouts

@router.post("/workouts", response_model=WorkoutOutSchema)
async def create_workout(
    workout_in: WorkoutCreateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
    ):

    workout = Workout(name=workout_in.name, date=datetime.now())
    current_user.workouts.append(workout)
    db.commit()

    return workout

@router.get("/workouts/{workout_id}", response_model=WorkoutOutSchema)
async def get_workout(workout_id: int, current_workout: Annotated[Workout, Depends(get_current_workout)]):
    return current_workout

@router.patch("/workouts/{workout_id}", response_model=WorkoutOutSchema)
async def update_workout(
    workout_id: int,
    workout: WorkoutUpdateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_workout: Annotated[Workout, Depends(get_current_workout)]
    ):

    for var, value in vars(workout).items():
        setattr(current_workout, var, value) if value else None
    db.commit()

    return current_workout

@router.delete("/workouts/{workout_id}", response_model=WorkoutOutSchema)
async def remove_workout(
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_workout: Annotated[Workout, Depends(get_current_workout)]
    ):

    db.delete(current_workout)
    db.commit()

    return current_workout

@router.post("/workouts/{workout_id}/copy", response_model=WorkoutOutSchema)
async def copy_workout(
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    current_workout: Annotated[Workout, Depends(get_current_workout)]
    ):
    """
    Deep copy of specified workout and setting of parent-child relationship
    at all levels (workout, exercise and set).
    """
    workout_copy = Workout(name=f"{current_workout.name}(Copy)", date=datetime.now(), parent_workout_id=current_workout.id)
    current_user.workouts.append(workout_copy)
    db.commit()
    for exercise in current_workout.exercises:
        exercise_copy = Exercise(name=exercise.name, parent_exercise_id=exercise.id)
        workout_copy.exercises.append(exercise_copy)
        db.commit()
        for set in exercise.sets:
            set_copy = Set(repetitions=set.repetitions, weight=set.weight, parent_set_id=set.id)
            exercise_copy.sets.append(set_copy)
            db.commit()

    return workout_copy