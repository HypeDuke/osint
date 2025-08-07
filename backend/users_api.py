from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, get_db
from pydantic import BaseModel
from typing import List

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

users_router = APIRouter()

@users_router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@users_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
