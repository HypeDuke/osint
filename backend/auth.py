from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from models import User, get_db
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

auth_router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

class UserSchema(BaseModel):
    username: str
    password: str

@auth_router.post("/register")
def register(user: UserSchema, db=Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = bcrypt.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    return {"msg": "Registered"}

@auth_router.post("/login")
def login(user: UserSchema, db=Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not bcrypt.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=2)},
        SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}
