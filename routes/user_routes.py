from fastapi import APIRouter
from sqlalchemy.orm import Session
from db import get_db
from fastapi import Depends
from repositories.User_repo import UserRepo
from schemas.User_schema import UserSchema

router = APIRouter()

@router.post("/signup")
def signup(user:User,db: Session=Depends(get_db)): 
    user_repo=UserRepo(db)
    user_repo.add_user()
    return {"message": "User signed up successfully"}

@router.post("/login")
def login():
    return {"message": "User logged in successfully"}
