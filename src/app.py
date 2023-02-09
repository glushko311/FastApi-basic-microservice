import secrets
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.schemas import User as UserSchema
from src.models import User

from src.db import get_db

security = HTTPBasic()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Phonebook"}


@app.get("/smoke")
async def smoke():
    return {"message": "smoke complete"}


async def authenticate(credential: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credential.username, 'unicorn')
    is_password_ok = secrets.compare_digest(credential.password, 'rainbow')
    if not (is_user_ok and is_password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"}
        )


@app.post("/user", response_model=UserSchema, dependencies=[Depends(authenticate)])
async def add_user(user: UserSchema, db: Session = Depends(get_db)):
    return User.create_user(db=db, user=user)


@app.get("/user", response_model=UserSchema, dependencies=[Depends(authenticate)])
async def get_user(last_name: str, db: Session = Depends(get_db)):
    response = User.get_user_by_lastname(db=db, lastname=last_name)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"User with lastname {last_name} not found")
