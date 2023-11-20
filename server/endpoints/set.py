from typing import List, Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from models import Exercise, Set
from schemas import SetCreateSchema, SetUpdateSchema, SetOutSchema
from deps import get_db, get_current_exercise, get_current_set

router = APIRouter()

@router.post("/workouts/{workout_id}/exercises/{exercise_id}/sets", response_model=SetOutSchema)
async def create_set(
    workout_id: int,
    exercise_id: int, set_in: SetCreateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_exercise: Annotated[Exercise, Depends(get_current_exercise)]
    ):

    set = Set(repetitions=set_in.repetitions, weight=set_in.weight)
    current_exercise.sets.append(set)
    db.commit()

    return set

@router.get("/workouts/{workout_id}/exercises/{exercise_id}/sets", response_model=List[SetOutSchema])
async def get_sets(
    exercise_id: int,
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_exercise: Annotated[Exercise, Depends(get_current_exercise)]
    ):

    sets_out: List[SetOutSchema] = []
    for set in current_exercise.sets:
        set_out = SetOutSchema(id=set.id, repetitions=set.repetitions, weight=set.weight)
        if set.parent_set_id is not None:
            parent_set = db.query(Set).filter(Set.id == set.parent_set_id).first()
            set_out.repetitions_diff = set.repetitions - parent_set.repetitions
            set_out.weight_diff      = set.weight - parent_set.weight
        sets_out.append(set_out) 

    return sets_out

@router.get("/workouts/{workout_id}/exercises/{exercise_id}/sets/{set_id}", response_model=SetOutSchema)
async def get_set(
    set_id: int,
    exercise_id: int,
    workout_id: int,
    current_set: Annotated[Set, Depends(get_current_set)]
    ):

    return current_set

@router.patch("/workouts/{workout_id}/exercises/{exercise_id}/sets/{set_id}", response_model=SetOutSchema)
async def update_set(
    set_id: int,
    exercise_id: int,
    workout_id: int,
    set: SetUpdateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_set: Annotated[Set, Depends(get_current_set)]
    ):

    for var, value in vars(set).items():
        setattr(current_set, var, value) if value else None
    db.commit()
    set_out = SetOutSchema(id=current_set.id, repetitions=current_set.repetitions, weight=current_set.weight)
    if current_set.parent_set_id is not None:
        parent_set = db.query(Set).filter(Set.id == current_set.parent_set_id).first()
        set_out.repetitions_diff = current_set.repetitions - parent_set.repetitions
        set_out.weight_diff      = current_set.weight - parent_set.weight 

    return set_out

@router.delete("/workouts/{workout_id}/exercises/{exercise_id}/sets/{set_id}", response_model=SetOutSchema)
async def remove_set(
    set_id: int,
    exercise_id: int,
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_set: Annotated[Set, Depends(get_current_set)]
    ):

    db.delete(current_set)
    db.commit()

    return current_set