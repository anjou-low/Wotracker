from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

    workouts: Mapped[List["Workout"]] = relationship(back_populates="user", cascade="all, delete")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r})"

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    date: Mapped[datetime]

    user_id = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(back_populates="workouts")
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="workout", cascade="all, delete")

    parent_workout_id: Mapped[Optional[int]] = mapped_column(ForeignKey("workouts.id", ondelete="SET NULL"))
    child_workout_id: Mapped[Optional[int]]  = mapped_column(ForeignKey("workouts.id", ondelete="SET NULL"))

    def __repr__(self) -> str:
        return f"Workout(id={self.id!r}, name={self.name!r}, date={self.date!r}, user_id={self.user_id!r}, parent_workout_id={self.parent_workout_id!r}, child_workout_id={self.child_workout_id!r})"

class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    workout_id = mapped_column(ForeignKey("workouts.id"))

    workout: Mapped[Workout] = relationship(back_populates="exercises")
    sets: Mapped[List["Set"]] = relationship(back_populates="exercise", cascade="all, delete")

    parent_exercise_id: Mapped[Optional[int]] = mapped_column(ForeignKey("exercises.id", ondelete="SET NULL"))

    def __repr__(self) -> str:
        return f"Exercise(id={self.id!r}, name={self.name!r}, workout_id={self.workout_id!r}, parent_exercise_id={self.parent_exercise_id!r})"

class Set(Base):
    __tablename__ = "sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    repetitions: Mapped[int]
    weight: Mapped[float]

    exercise_id   = mapped_column(ForeignKey("exercises.id"))

    exercise: Mapped[Exercise] = relationship(back_populates="sets")

    parent_set_id: Mapped[Optional[int]] = mapped_column(ForeignKey("sets.id", ondelete="SET NULL"))

    def __repr__(self) -> str:
        return f"Set(id={self.id!r}, repetitions={self.repetitions!r}, weight={self.weight!r}, exercise_id={self.exercise_id!r}, parent_set_id={self.parent_set_id!r})"