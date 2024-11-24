from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, unique=True, index=True)
    username = Column(String(length=12), unique=True, index=True)
    password = Column(String, nullable=False)

    session = relationship("Session", uselist=False, back_populates="user")
    tasks = relationship("Task", uselist=True, back_populates="user")
    created_at = Column(DateTime(timezone=True), default=func.now())

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, index=True)
    token_id = Column(UUID(as_uuid=True), nullable=True, index=True, default=None)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"),
        primary_key=True,
        unique=True
    )
    
    user = relationship("User", back_populates="session")
    expires_at = Column(DateTime(timezone=True), nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    title = Column(String)
    user = relationship("User", back_populates="tasks") 
    created_at = Column(DateTime(timezone=True), default=func.now())