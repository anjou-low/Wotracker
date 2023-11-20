from typing import Annotated, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from security import decode_access_token
from models import User, Workout, Exercise, Set
from db import SessionLocal

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")

async def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
    ) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    sub = decode_access_token(token)
    if sub is None:
        raise credentials_exception
    user_id: int = int(sub) 
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_workout(
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
    ) -> Workout:

    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if workout is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This workout does not exist."
        )
    if workout.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials for accessing this workout."
        )
    return workout

async def get_current_exercise(
    exercise_id: int, workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_workout: Annotated[Workout, Depends(get_current_workout)]
    ) -> Exercise:

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This exercise does not exist."
        )
    if exercise.workout_id != current_workout.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials for accessing this exercise",
        )
    return exercise

async def get_current_set(
    set_id: int,
    exercise_id: int,
    workout_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_exercise: Annotated[Exercise, Depends(get_current_exercise)]
    ) -> Set:

    set = db.query(Set).filter(Set.id == set_id).first()
    if set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This set does not exist."
        )
    if set.exercise_id != current_exercise.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials for accessing this set."
        )
    return set