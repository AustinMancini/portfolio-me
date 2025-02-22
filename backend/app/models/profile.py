import uuid
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID  # Use the PostgreSQL UUID type
from core.config import Base

# Create the Profile model
class Profile(Base):
    __tablename__ = 'profiles'
    # Use Uuid without ForeignKey; the constraint will be added in Supabase
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True, index=True)
    is_subscribed = Column(Boolean, default=False)
    role = Column(String, default='user')