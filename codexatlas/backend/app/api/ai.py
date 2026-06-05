from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class AIRequest(BaseModel):
    repoId: str
    question: str

class AIResponse(BaseModel):
    answer: str
    context: list

@router.post("/ask", response_model=AIResponse)
async def ask_ai(request: AIRequest):
    """Ask a repository-aware question to the AI"""
    try:
        # Mock AI response
        return AIResponse(
            answer=f"Based on the analysis of this repository, here's the answer to your question: {request.question}\n\nThe repository uses React with TypeScript and follows a component-based architecture. The main entry point is src/App.tsx, and the application is organized with separate folders for components, pages, and services.",
            context=[
                "src/App.tsx",
                "src/components/",
                "src/pages/",
                "src/services/"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
