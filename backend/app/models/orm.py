from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    repo_url = Column(String)
    status = Column(String) # "processing", "completed", "failed"
    data = Column(JSON, nullable=True) # Will hold graph, health, architecture
    created_at = Column(DateTime(timezone=True), server_default=func.now())
