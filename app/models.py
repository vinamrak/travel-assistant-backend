from sqlmodel import SQLModel, Field
from typing import Optional

class UserPreference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    destination: str
    budget: float
    travel_dates: str
    notes: Optional[str] = None
