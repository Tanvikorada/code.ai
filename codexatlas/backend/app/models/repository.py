from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Repository(BaseModel):
    id: str
    name: str
    url: str
    framework: str = ""
    language: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RepositoryCreate(BaseModel):
    url: str

class RepositoryResponse(BaseModel):
    id: str
    name: str
    url: str
    framework: str
    language: str
    created_at: str
