# app/api/profile.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.config import get_session
from app.core.security import get_current_user
from app.models.profile import Profile  # Your SQLAlchemy Profile model
from app.schemas.profile import ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["profiles"])

# Dependency for subscriber-only access
def get_current_subscriber_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "subscriber":
        raise HTTPException(status_code=403, detail="Not authorized as a subscriber")
    return current_user

# Dependency for admin-only access
def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized as an admin")
    return current_user

# Subscriber: View own profile
@router.get("/me", response_model=ProfileResponse)
def get_own_profile(current_user: dict = Depends(get_current_subscriber_user), db: Session = Depends(get_session)):
    profile = db.query(Profile).filter(Profile.user_id == current_user["user_id"]).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# Subscriber: Update own profile (limited to is_subscribed)
@router.put("/me", response_model=ProfileResponse)
def update_own_profile(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_subscriber_user),
    db: Session = Depends(get_session)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user["user_id"]).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile_data.is_subscribed is not None:
        profile.is_subscribed = profile_data.is_subscribed
    # Prevent subscribers from changing their role
    if profile_data.role and profile_data.role != profile.role:
        raise HTTPException(status_code=403, detail="Subscribers cannot change roles")
    db.commit()
    db.refresh(profile)
    return profile

# Admin: View any profile
@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile_by_id(
    user_id: UUID,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_session)
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# Admin: Update any profile
@router.put("/{user_id}", response_model=ProfileResponse)
def update_profile_by_id(
    user_id: UUID,
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_session)
):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile_data.is_subscribed is not None:
        profile.is_subscribed = profile_data.is_subscribed
    if profile_data.role in ["subscriber", "admin"]:
        profile.role = profile_data.role
    db.commit()
    db.refresh(profile)
    return profile