# app/schemas/profile.py
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from typing import Literal

# Base schema with shared profile fields
class ProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    is_subscribed: bool | None = None
    # could be is_subscribed: bool | None. I will test and see what happens

# Schema for updating profile information
class ProfileUpdate(ProfileBase):
    role: Literal["subscriber", "admin"]

# Schema for profile response data
class ProfileResponse(ProfileBase):
    user_id: UUID
    is_subscribed: bool
    role: Literal["subscriber", "admin"]


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    role: Literal["subscriber", "admin"]