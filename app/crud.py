from fastapi import HTTPException
from sqlmodel import Session, select
from .models import UserPreference

def create_preference(pref: UserPreference, session: Session):
    session.add(pref)
    session.commit()
    session.refresh(pref)
    return pref

def get_all_preferences(session: Session):
    return session.exec(select(UserPreference)).all()

def update_preference(pref_id: int, update_data: UserPreference, session: Session):
    pref = session.get(UserPreference, pref_id)
    if not pref:
        raise HTTPException(404, detail="Preference not found")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(pref, key, value)
    session.commit()
    return pref

def delete_preference(pref_id: int, session: Session):
    pref = session.get(UserPreference, pref_id)
    if not pref:
        raise HTTPException(404, detail="Preference not found")
    session.delete(pref)
    session.commit()
