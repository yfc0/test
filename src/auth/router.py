from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, status

from typing import Annotated

from utils.schemas import CreateUser, AuthUser
from services.auth import AuthService
from db.session import get_session

from auth.oauth2 import create_access_token

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/register")
async def register_user(user: CreateUser,  session = Depends(get_session)):
    await AuthService(session).validate_registation_user(user)
    await AuthService(session).create_user(user)
    return {"message": "200"}


@router.post("/login")
async def login(user: AuthUser, session = Depends(get_session)):
    user_id = await AuthService(session).check_user(user)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not found user")

    if not await AuthService(session).check_password(user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Error password")

    access_token = create_access_token(data={"user_id": user_id})

    return {"access_token": access_token, "token_type": "bearer"}
