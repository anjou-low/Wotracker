from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    username: str
    password: str

class UserUpdateSchema(BaseModel):
    id: int
    username: Optional[str]

class UserOutSchema(BaseModel):
    id: int
    username: str

class WorkoutCreateSchema(BaseModel):
    name: str

class WorkoutUpdateSchema(BaseModel):
    name: str | None = None
    date: str | None = None

class WorkoutOutSchema(BaseModel):
    id: int
    name: str
    date: datetime

class ExerciseCreateSchema(BaseModel):
    name: str
    tags: Optional[List[str]]

class ExerciseUpdateSchema(BaseModel):
    name: str | None = None

class ExerciseOutSchema(BaseModel):
    id: int
    name: str

class SetCreateSchema(BaseModel):
    repetitions: int
    weight: float

class SetUpdateSchema(BaseModel):
    repetitions: int | None = None
    weight: float | None = None

class SetOutSchema(BaseModel):
    id: int
    repetitions: int
    weight: float
    repetitions_diff: int | None = None
    weight_diff: float | None = None