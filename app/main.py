from fastapi import FastAPI
from app.db import get_all_incidents
from app.models import Incident
from typing import List

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TripleZero Ops API is running"}

@app.get("/incidents")
def show_incidents() -> List[Incident]:
    return get_all_incidents()