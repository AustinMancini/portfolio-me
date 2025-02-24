import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID 
from app.core.config import Base

class Profile(Base):
    __tablename__ = 'profiles'
    __table_args__ = {'schema': 'public'}
    # Use Uuid without ForeignKey; the constraint will be added in Supabase
    user_id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True, index=True)
    is_subscribed = Column(Boolean, default=False)
    role = Column(String, default='user')