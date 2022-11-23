from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    picture = Column(String, default=None)
    last_login_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    items = relationship('Item', back_populates='owner')

