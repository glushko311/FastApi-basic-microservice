from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config import ACCESS_TOKEN_EXPIRE_MINUTES, VERSION_PREFIX
from src.database import get_session
from src.auth_tools import create_access_token
from src.auth.managers import SessionManager, UserManager
from src.auth.schemas import TokenSchema, UserRegSchema
from src.auth.schemas import UserSchema

auth_router = APIRouter(
    prefix=f"{VERSION_PREFIX}/auth",
    tags=["auth"]
)

user_router = APIRouter(
    prefix=f"{VERSION_PREFIX}/user",
    tags=["user"]
)


@auth_router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):

    user = await UserManager.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    await SessionManager.update_session(db, user, access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(UserManager.get_current_active_user)):
    json_compatible_item_data = jsonable_encoder(current_user)
    return JSONResponse(content=json_compatible_item_data)


@user_router.post("", response_model=UserRegSchema)
async def add_user(user: UserRegSchema, db: AsyncSession = Depends(get_session)):

    user = await UserManager.create_user(db=db, user=user)
    json_compatible_item_data = jsonable_encoder(user)
    return JSONResponse(content=json_compatible_item_data)
