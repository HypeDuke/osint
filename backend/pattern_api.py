from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

pattern_router = APIRouter()
PATTERN_PATH = "./patterns/patterns.json"

class PatternSchema(BaseModel):
    pattern: str

@pattern_router.get("/")
def list_patterns():
    if not os.path.exists(PATTERN_PATH):
        return []
    with open(PATTERN_PATH, "r") as f:
        return json.load(f)

@pattern_router.post("/")
def add_pattern(p: PatternSchema):
    patterns = list_patterns()
    if p.pattern in patterns:
        raise HTTPException(status_code=400, detail="Pattern exists")
    patterns.append(p.pattern)
    with open(PATTERN_PATH, "w") as f:
        json.dump(patterns, f)
    return {"msg": "Pattern added"}

@pattern_router.delete("/")
def delete_pattern(p: PatternSchema):
    patterns = list_patterns()
    if p.pattern not in patterns:
        raise HTTPException(status_code=404, detail="Pattern not found")
    patterns.remove(p.pattern)
    with open(PATTERN_PATH, "w") as f:
        json.dump(patterns, f)
    return {"msg": "Pattern deleted"}
