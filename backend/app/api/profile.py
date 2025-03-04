from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.profile import ProfileResponse
from backend.app.core.auth import get_current_subscriber_user

# Used to create a new route for the endpoint /profiles/me.
router = APIRouter(prefix="/profiles", tags=["profiles"])

#endpoint to return user profile information
@router.get("/me", response_model=ProfileResponse)
async def get_own_profile(current_user: ProfileResponse = Depends(get_current_subscriber_user)):
    return current_user