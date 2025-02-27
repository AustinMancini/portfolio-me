import uuid
from sqlalchemy import Column, String, Boolean, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from app.core.config import Base

# Dummy User model for auth.users (Supabase-managed)
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "auth"}
    id = Column(UUID(as_uuid=True), primary_key=True)

class Profile(Base):
    __tablename__ = 'profiles'
    __table_args__ = (
        CheckConstraint("role IN ('subscriber', 'admin')", name="valid_role"),
        {"schema": "public"}
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        primary_key=True
    )
    full_name = Column(String, nullable=True, index=True)
    is_subscribed = Column(Boolean, default=False)
    role = Column(String, default='subscribers')