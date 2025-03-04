from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.profile import ProfileResponse
from backend.app.core.auth import get_current_user

# Used to create a new route for the endpoint /profiles/me.
router = APIRouter(prefix="/profiles", tags=["profiles"])

#endpoint to return user profile information
@router.get("/me", response_model=ProfileResponse)
async def read_users_me(current_user: Annotated[ProfileResponse, Depends(get_current_user)]):
    return current_user