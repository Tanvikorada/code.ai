from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class DocumentationRequest(BaseModel):
    repoId: str

class DocumentationResponse(BaseModel):
    readme: str
    architecture_docs: str
    api_docs: str
    setup_guide: str

@router.post("/generate", response_model=DocumentationResponse)
async def generate_documentation(request: DocumentationRequest):
    """Generate documentation for a repository"""
    try:
        return DocumentationResponse(
            readme="# Project README\n\nThis is an automatically generated README.",
            architecture_docs="# Architecture Documentation\n\n## System Overview\n\nThe system is organized into multiple layers...",
            api_docs="# API Documentation\n\n## Endpoints\n\n### POST /api/scan\nScan a GitHub repository.",
            setup_guide="# Setup Guide\n\n## Installation\n\n```bash\nnpm install\n```\n\n## Running\n\n```bash\nnpm run dev\n```"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
