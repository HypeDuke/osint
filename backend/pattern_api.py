from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

pattern_router = APIRouter()
PATTERN_PATH = "./patterns/patterns.json"

class PatternSchema(BaseModel):
    pattern: str

def load_patterns():
    if not os.path.exists(PATTERN_PATH):
        return []
    with open(PATTERN_PATH, "r") as f:
        data = json.load(f)
        return data.get("patterns", [])

def save_patterns(patterns):
    with open(PATTERN_PATH, "w") as f:
        json.dump({"patterns": patterns}, f, indent=2)

def generate_new_id(patterns):
    existing_ids = [int(p["id"][1:]) for p in patterns if p["id"].startswith("P")]
    next_id = max(existing_ids, default=0) + 1
    return f"P{str(next_id).zfill(3)}"

@pattern_router.get("/")
def list_patterns():
    return load_patterns()

@pattern_router.post("/")
def add_pattern(p: PatternSchema):
    patterns = load_patterns()
    if any(p.pattern == pat["pattern"] for pat in patterns):
        raise HTTPException(status_code=400, detail="Pattern already exists")
    new_id = generate_new_id(patterns)
    patterns.append({"id": new_id, "pattern": p.pattern})
    save_patterns(patterns)
    return {"msg": "Pattern added", "id": new_id}

@pattern_router.delete("/")
def delete_pattern(p: PatternSchema):
    patterns = load_patterns()
    filtered = [pat for pat in patterns if pat["pattern"] != p.pattern]
    if len(filtered) == len(patterns):
        raise HTTPException(status_code=404, detail="Pattern not found")
    save_patterns(filtered)
    return {"msg": "Pattern deleted"}
