import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from backend.app.core.config import get_session
from backend.app.schemas.profile import ProfileResponse
from backend.app.models.profile import Profile
from supabase import AsyncClientOptions
from supabase._async.client import AsyncClient, create_client

load_dotenv()

async def get_supabase_client() -> AsyncClient:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    # Create an async Supabase client with custom timeout settings
    supabase = await create_client(
        url,
        key,
        options=AsyncClientOptions(
            postgrest_client_timeout=10,
        )
    )
    if not supabase:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Supabase client not initialized")
    return supabase

# Type annotation for dependency injection of Supabase client
SupabaseClient = Annotated[AsyncClient, Depends(get_supabase_client)]

# Define JWT authentication scheme that expects Bearer tokens
jwt_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def get_current_user(token: Annotated[str, Depends(jwt_scheme)], supabase: SupabaseClient, db=Depends(get_session)) -> ProfileResponse:
    """
    Validates the JWT token and retrieves the current user's profile.
    
    Args:
        token (str): JWT token from the Authorization header
        supabase (AsyncClient): Initialized Supabase client
        db (Session): Database session for SQLAlchemy queries
        
    Returns:
        ProfileResponse: Pydantic model containing user profile information
        
    Raises:
        HTTPException: 
            - 401 if authentication fails
            - 404 if user profile not found
            - 500 for other internal errors
    """
    try:
        # Verify JWT token and get user information from Supabase
        user_response = await supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        
        # Extract user ID from the verified token response
        user_id = user_response.user.id
        
        # Query the Supabase db for user's profile information 
        user_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if user_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in database")

        # Return a Pydantic model
        return ProfileResponse(
            user_id=user_profile.user_id,
            is_subscribed=user_profile.is_subscribed,
            role=user_profile.role
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")
    

async def get_current_subscriber_user(current_user: ProfileResponse = Depends(get_current_user)) -> ProfileResponse:
    """Restrict access to users with the 'subscriber' role."""
    if current_user.role != "subscriber":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as a subscriber")
    return current_user