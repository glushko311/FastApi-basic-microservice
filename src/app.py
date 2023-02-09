from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from src.schemas import User as UserSchema
from src.models import User
# from src.crud import get_user_by_lastname, create_user
from src.db import get_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Phonebook"}


@app.get("/smoke")
async def smoke():
    return {"message": "smoke complete"}


@app.post("/user", response_model=UserSchema)
async def add_user(user: UserSchema, db: Session = Depends(get_db)):
    return User.create_user(db=db, user=user)


@app.get("/user", response_model=UserSchema)
async def get_user(last_name: str, db: Session = Depends(get_db)):
    response = User.get_user_by_lastname(db=db, lastname=last_name)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"User with lastname {last_name} not found")
