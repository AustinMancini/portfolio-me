import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from app.core.config import Base
from datetime import datetime, timezone

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = {'schema': 'public'}
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('public.profiles.user_id'), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)