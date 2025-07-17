from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.models import UserPreference
from app.database import create_db_and_tables, get_session
from app.auth import verify_api_key
from app.crud import create_preference, get_all_preferences, update_preference, delete_preference
from app.utils import summarize_preferences

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/preferences/", dependencies=[Depends(verify_api_key)])
def create(pref: UserPreference, session: Session = Depends(get_session)):
    return create_preference(pref, session)

@app.get("/preferences/", dependencies=[Depends(verify_api_key)])
def read(session: Session = Depends(get_session)):
    return get_all_preferences(session)

@app.put("/preferences/{pref_id}", dependencies=[Depends(verify_api_key)])
def update(pref_id: int, data: UserPreference, session: Session = Depends(get_session)):
    return update_preference(pref_id, data, session)

@app.delete("/preferences/{pref_id}", dependencies=[Depends(verify_api_key)])
def delete(pref_id: int, session: Session = Depends(get_session)):
    return delete_preference(pref_id, session)

@app.post("/transform/", dependencies=[Depends(verify_api_key)])
def transform(data: UserPreference):
    return {"summary": summarize_preferences(data)}

@app.get("/ping")
def ping():
    return {"status": "ok"}
