from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from app.models import UserPreference
from app.database import create_db_and_tables, get_session
from app.auth import verify_api_key
from app.crud import create_preference, get_all_preferences, update_preference, delete_preference
from app.utils import summarize_preferences
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

class HotelRequest(BaseModel):
    destination: str
    budget: float
    travel_dates: str

class HotelOption(BaseModel):
    name: str
    price_per_night: float
    rating: float

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


@app.post("/recommend_hotels", response_model=List[HotelOption], dependencies=[Depends(verify_api_key)])
def recommend_hotels(data: HotelRequest):
    try:
        start_str, end_str = data.travel_dates.split(" to ")
        start = datetime.strptime(start_str.strip(), "%Y-%m-%d")
        end = datetime.strptime(end_str.strip(), "%Y-%m-%d")
        nights = (end - start).days
        if nights <= 0:
            return ValueError("Invalid travel date range")

        max_per_night = data.budget / nights

        # Dummy hotel data
        hotels = [
            {"name": "Hotel Lotus", "price_per_night": 580, "rating": 4.5},
            {"name": "Palm Suites", "price_per_night": 620, "rating": 4.2},
            {"name": "Rama Inn", "price_per_night": 590, "rating": 4.7},
            {"name": "CheapStay", "price_per_night": 300, "rating": 3.8},
            {"name": "Grand Elite", "price_per_night": 1000, "rating": 4.9}
        ]

        filtered = [h for h in hotels if h["price_per_night"] <= max_per_night]
        top_3 = sorted(filtered, key=lambda h: -h["rating"])[:3]
        return top_3

    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

