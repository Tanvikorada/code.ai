from pydantic import BaseModel
from typing import Optional, Literal

class Node(BaseModel):
    id: str
    repo_id: str
    node_type: Literal["file", "component", "function", "api", "database", "service", "hook", "class"]
    name: str
    path: Optional[str] = None
    complexity: Optional[int] = 0

class Edge(BaseModel):
    id: str
    source: str
    target: str
    relationship: Literal["imports", "calls", "returns", "creates", "updates", "reads", "writes", "depends_on"]
