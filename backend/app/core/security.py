import jwt, os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from backend.app.core.config import SUPABASE_JWT_SECRET, get_session
from backend.app.schemas.profile import ProfileResponse
from backend.app.models.profile import Profile
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Define JWT header scheme (expects "Authorization: Bearer <token>")
jwt_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def get_current_user(token: str = Depends(jwt_scheme), db=Depends(get_session)) -> ProfileResponse:
    """
    Authenticate the user with Supabase and retrieve their profile.
    
    Args:
        token: JWT from the Authorization header
        db: Database session dependency
    
    Returns:
        ProfileResponse: Pydantic model with user profile data
    
    Raises:
        HTTPException: If authentication or profile retrieval fails
    """
    # Check if token is provided
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")

    try:
        # Verify the token and get the user directly
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: user not found")
        
        # Extract user ID from the response
        user_id = user_response.user.id
        print(f"Authenticated user ID: {user_id}")  # Debug

        # Fetch the profile from the database
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

        # Return the profile as a Pydantic model
        return ProfileResponse(
            user_id=profile.user_id,
            is_subscribed=profile.is_subscribed,
            role=profile.role
        )

    except Exception as e:
        print(f"Error during authentication: {e}")  # Add logging for debugging
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")