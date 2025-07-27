from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import redis
import json
import requests

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB setup
SQLALCHEMY_DATABASE_URL = "postgresql://admin:adminpass@postgres:5432/users_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis setup
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Elasticsearch setup
ELASTICSEARCH_URL = "http://elasticsearch:9200/leaks/_search"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class SearchQuery(BaseModel):
    keyword: str

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth utils

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Routes
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/search")
def search(query: SearchQuery):
    keyword = query.keyword
    redis_key = f"search:{keyword}"

    # Check cache first
    if redis_client.exists(redis_key):
        return {"cached": True, "results": json.loads(redis_client.get(redis_key))}

    # Otherwise query Elasticsearch
    es_query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["raw_data", "emails", "domain"]
            }
        }
    }
    response = requests.post(ELASTICSEARCH_URL, json=es_query)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Elasticsearch error")

    hits = response.json().get("hits", {}).get("hits", [])
    results = [hit["_source"] for hit in hits]

    redis_client.setex(redis_key, 3600, json.dumps(results))
    return {"cached": False, "results": results}
