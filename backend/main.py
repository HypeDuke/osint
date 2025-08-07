from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import auth_router
from pattern_api import pattern_router
from es_search import es_router
from users_api import users_router

app = FastAPI()

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(auth_router, prefix="/auth")
app.include_router(pattern_router, prefix="/patterns")
app.include_router(es_router, prefix="/search")
app.include_router(users_router, prefix="/users")
