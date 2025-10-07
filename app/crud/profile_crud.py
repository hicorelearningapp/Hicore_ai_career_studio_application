from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.profile import Profile

def create_profile(db: Session, profile_data: dict):
    profile = Profile(**profile_data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profiles(db: Session):
    return db.query(Profile).all()

def get_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

def update_profile(db: Session, profile_id: int, data: dict):
    profile = get_profile(db, profile_id)
    for key, value in data.items():
        if hasattr(profile, key):
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, profile_id: int):
    profile = get_profile(db, profile_id)
    db.delete(profile)
    db.commit()
    return {"detail": "Profile deleted successfully"}
