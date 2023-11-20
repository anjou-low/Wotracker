from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from schemas import UserCreateSchema, UserOutSchema
from deps import get_db
from security import get_password_hash, verify_password, generate_access_token
from config import settings

router = APIRouter()

@router.post("/users", response_model=UserOutSchema)
async def create_user(
    user_in: UserCreateSchema,
    db: Annotated[Session, Depends(get_db)]
    ):

    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is associated with an existing account."
        )
    user = User(username=user_in.username, password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()

    return user

@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
    ):

    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
    access_token = generate_access_token(
        user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token": "bearer"}