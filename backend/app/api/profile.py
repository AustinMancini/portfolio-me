from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.profile import ProfileResponse
from backend.app.core.security import get_current_user

# Used to create a new route for the endpoint /profiles/me.
router = APIRouter(prefix="/profiles", tags=["profiles"])


# GET /profiles/me: Allows subscribers to view their own profile.
#1. Create a new route for the endpoint /profiles/me.
#2. Add a GET method to the new route.
#3. Get the user's profile from the database.
#4. Return the user's profile.
@router.get("/me", response_model=ProfileResponse)
async def get_own_profile(current_user: ProfileResponse = Depends(get_current_user)):
    """Return the authenticated user's profile."""
    return current_user

# PUT /profiles/me: Allows subscribers to update their own profile (e.g., toggle is_subscribed).

# GET /profiles/{user_id}: Allows admins to view any profile.

# PUT /profiles/{user_id}: Allows admins to update any profile (e.g., change roles or subscription status).