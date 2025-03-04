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
    supabase = await create_client(
        url,
        key,
        options=AsyncClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10
        )
    )
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized")
    return supabase

SupabaseClient = Annotated[AsyncClient, Depends(get_supabase_client)]


# Define JWT header scheme (expects "Authorization: Bearer <token>")
jwt_scheme = APIKeyHeader(name="Authorization", auto_error=False)

async def get_current_user(token: Annotated[str, Depends(jwt_scheme)], supabase: SupabaseClient, db=Depends(get_session)) -> ProfileResponse:
    try:

        # check the JWT token for the user_id
        user_response = await supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        
        # grab the user id from the user_response and use that to query the user in the database
        user_id = user_response.user.id
        
        # query the database with the user_id 
        user_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if user_profile is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in database")

        # Return a pydantic model response
        return ProfileResponse(
            user_id=user_profile.user_id,
            is_subscribed=user_profile.is_subscribed,
            role=user_profile.role
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")