from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import httpx

from app.database import get_db
from app.models.orm import ScanResult, User
from app.core.dependencies import get_current_user

router = APIRouter()

class AIRequest(BaseModel):
    repoId: str
    question: str

class AIResponse(BaseModel):
    answer: str
    context: list

@router.post("/ask", response_model=AIResponse)
async def ask_ai(
    request: AIRequest,
    fastapi_req: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ask a repository-aware question to the AI"""
    scan = db.query(ScanResult).filter(ScanResult.id == request.repoId, ScanResult.user_id == current_user.id).first()
    if not scan or not scan.data:
        raise HTTPException(status_code=404, detail="Repository scan data not found or not completed")
        
    metadata = scan.data.get("metadata", {})
    health = scan.data.get("health", {})
    arch = scan.data.get("architecture", {})
    
    # Extract file list
    nodes = scan.data.get("graph", {}).get("nodes", [])
    files = [n.get("path") for n in nodes if n.get("node_type") == "file"]
    classes = [n.get("name") for n in nodes if n.get("node_type") == "class"]
    functions = [n.get("name") for n in nodes if n.get("node_type") == "function"]
    
    # Build prompt context
    context_summary = f"Repository Name: {metadata.get('name')}\n"
    context_summary += f"URL: {metadata.get('url')}\n"
    context_summary += f"Primary Language: {metadata.get('language')}\n"
    context_summary += f"Framework: {metadata.get('framework')}\n"
    context_summary += f"Health Score: {health.get('overall_score')}/100\n"
    
    context_summary += "\nArchitecture Layers:\n"
    for layer in arch.get("layers", []):
        context_summary += f"- {layer.get('name')}: {', '.join(layer.get('components', []))}\n"
        
    context_summary += f"\nFiles (up to 30): {', '.join(files[:30])}\n"
    
    custom_api_key = fastapi_req.headers.get("x-custom-api-key")
    if custom_api_key:
        if custom_api_key.startswith("gsk_"):
            GROQ_API_KEY = custom_api_key
            GEMINI_API_KEY = None
        else:
            GEMINI_API_KEY = custom_api_key
            GROQ_API_KEY = None
    else:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    system_prompt = (
        "You are an expert Software Architect AI assistant for CodexAtlas. "
        "You answer questions about the codebases scanned by the user. "
        "Use the provided codebase metadata and file structure to give detailed, "
        "accurate, and helpful answers. Focus on code quality, architecture layers, "
        "dependencies, and structure."
    )
    user_prompt = f"Codebase Context:\n{context_summary}\n\nQuestion: {request.question}"

    last_error = None

    # Try Groq first
    if GROQ_API_KEY and not GROQ_API_KEY.startswith("your_"):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 1024
                    },
                    timeout=20.0
                )
                if response.status_code == 200:
                    res_data = response.json()
                    answer = res_data["choices"][0]["message"]["content"]
                    return AIResponse(answer=answer, context=files[:5])
                else:
                    last_error = f"Groq API error {response.status_code}: {response.text[:200]}"
        except Exception as e:
            last_error = f"Groq request failed: {str(e)}"

    # Try Gemini as fallback
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": f"System: {system_prompt}\n\nUser: {user_prompt}"}]}],
                        "generationConfig": {
                            "temperature": 0.2,
                            "maxOutputTokens": 1024
                        }
                    },
                    timeout=20.0
                )
                if response.status_code == 200:
                    res_data = response.json()
                    answer = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    return AIResponse(answer=answer, context=files[:5])
                else:
                    last_error = f"Gemini API error {response.status_code}: {response.text[:200]}"
        except Exception as e:
            last_error = f"Gemini request failed: {str(e)}"

    # Offline fallback with error details
    framework_info = f"using {metadata.get('framework')}" if metadata.get('framework') != 'unknown' else ""
    error_detail = f"\n\n**Error detail:** `{last_error}`" if last_error else ""
    fallback_answer = (
        f"**[Notice: Running in Offline Mode (no API Key set)]**\n\n"
        f"Based on the static analysis of **{metadata.get('name')}**, here is the structural context:\n"
        f"- **Language & Framework**: {metadata.get('language')} {framework_info}\n"
        f"- **Health Quality**: {health.get('overall_score')}/100 with maintainability score of {health.get('maintainability')}/100.\n"
        f"- **Identified Files**: The system analyzed {len(files)} file nodes, {len(classes)} class nodes, and {len(functions)} functions.\n\n"
        f"To enable full repository-aware conversational answers, please set a valid `GROQ_API_KEY` or `GEMINI_API_KEY` in the backend environment variables, "
        f"or click **Add Key** in the AI Assistant panel to use your own key.{error_detail}"
    )
    return AIResponse(
        answer=fallback_answer,
        context=files[:5]
    )


