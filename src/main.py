from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, status
from auth import router

from db.session import get_session
from auth.oauth2 import get_current_user

from services.auth import AuthService
from services.referral_code import RefferalCodeService
from services.user import UserService

from utils.schemas import CreateCode

app = FastAPI()

app.include_router(router.router)


@app.post("/create_code")
async def create_code(code: CreateCode, user = Depends(get_current_user),
                      session = Depends(get_session)):
    await RefferalCodeService(session).create(user, code.end_date)
    return {"code":"create"}


@app.put("/refresh_code")
async def refresh_code(code: CreateCode, user = Depends(get_current_user),
                      session = Depends(get_session)):
    await RefferalCodeService(session).refresh_code(user, code.end_date)
    return {"code":"refresh"}


@app.get("/referral_info")
async def referral_info(user_id: int, session = Depends(get_session)):
    users = await UserService(session).get_refferal_info(user_id)
    if not users:
        return {"status": "not found"}
    items = []
    for user in users:
        items.append({"username": user.username,
                      "email": user.email,
                      "code": user.referral_code})
    return items
