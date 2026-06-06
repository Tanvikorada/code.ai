from pydantic import BaseModel
from typing import Optional

class File(BaseModel):
    id: str
    repo_id: str
    path: str
    type: str
    complexity: Optional[int] = 0
    language: Optional[str] = ""
