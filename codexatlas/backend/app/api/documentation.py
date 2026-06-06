from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import httpx
import json

from app.database import get_db
from app.models.orm import ScanResult, User
from app.core.dependencies import get_current_user

router = APIRouter()

class DocumentationRequest(BaseModel):
    repoId: str

class DocumentationResponse(BaseModel):
    readme: str
    architecture_docs: str
    api_docs: str
    setup_guide: str

@router.post("/generate", response_model=DocumentationResponse)
async def generate_documentation(
    request: DocumentationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate documentation for a repository"""
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
    
    # Build codebase summary for prompt
    context_summary = f"Repository Name: {metadata.get('name')}\n"
    context_summary += f"URL: {metadata.get('url')}\n"
    context_summary += f"Primary Language: {metadata.get('language')}\n"
    context_summary += f"Framework: {metadata.get('framework')}\n"
    context_summary += f"Health Score: {health.get('overall_score')}/100\n"
    
    context_summary += "\nArchitecture Layers:\n"
    for layer in arch.get("layers", []):
        context_summary += f"- {layer.get('name')}: {', '.join(layer.get('components', []))}\n"
        
    context_summary += f"\nFiles: {', '.join(files[:30])}\n"
    
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
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
                        "response_format": {"type": "json_object"},
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert technical writer AI. "
                                    "Your job is to generate documentation for codebases. "
                                    "You must output a JSON object containing EXACTLY these keys: "
                                    "\"readme\", \"architecture_docs\", \"api_docs\", \"setup_guide\". "
                                    "All values must be detailed markdown strings tailored to the provided codebase context."
                                )
                            },
                            {
                                "role": "user",
                                "content": f"Generate documentation for this codebase:\n\n{context_summary}"
                            }
                        ],
                        "temperature": 0.2,
                        "max_tokens": 2048
                    },
                    timeout=25.0
                )
                if response.status_code == 200:
                    res_json = response.json()
                    content_str = res_json["choices"][0]["message"]["content"]
                    docs = json.loads(content_str)
                    return DocumentationResponse(
                        readme=docs.get("readme", ""),
                        architecture_docs=docs.get("architecture_docs", ""),
                        api_docs=docs.get("api_docs", ""),
                        setup_guide=docs.get("setup_guide", "")
                    )
        except Exception:
            pass

    # Dynamic Smart Fallback when Groq key is missing or failed
    repo_name = metadata.get("name", "Repository")
    lang = metadata.get("language", "Unknown")
    fw = metadata.get("framework", "Unknown")
    
    # Generate dynamic Setup Guide
    setup_commands = ""
    if lang.lower() == "python":
        setup_commands = "pip install -r requirements.txt\npython main.py"
    elif lang.lower() in ["javascript", "typescript"]:
        setup_commands = "npm install\nnpm run dev"
    else:
        setup_commands = "# Build and run instructions depend on environment\nmake build"
        
    dynamic_readme = f"""# {repo_name}
    
This project is built using **{lang}** with the **{fw}** framework.

## Key Features
* Dynamic codebase visualizer structure
* Automatically detected architecture components
* Automated health reports with score: **{health.get('overall_score', 100)}/100**

## Project Files Analyzed
{', '.join([f'`{f}`' for f in files[:10]])}
"""

    dynamic_arch = f"""# Architecture Documentation - {repo_name}

## Layout Overview
This system follows the layers detected below:

"""
    for layer in arch.get("layers", []):
        dynamic_arch += f"### {layer.get('name')}\n"
        dynamic_arch += f"Contains components: {', '.join([f'`{c}`' for c in layer.get('components', [])])}\n\n"

    dynamic_api = f"""# API & Components Reference - {repo_name}

## Classes Detected
{', '.join([f'* `{c}`' for c in classes]) if classes else "No classes found."}

## Functions / Methods Detected
{', '.join([f'* `{f}`' for f in functions[:15]]) if functions else "No functions found."}
"""

    dynamic_setup = f"""# Setup & Installation Guide - {repo_name}

## Prerequisites
* Ensure you have {lang} version installed.

## Getting Started
```bash
# Clone and enter directory
git clone {metadata.get('url', '')}
cd {repo_name}

# Install dependencies and start
{setup_commands}
```
"""

    return DocumentationResponse(
        readme=dynamic_readme,
        architecture_docs=dynamic_arch,
        api_docs=dynamic_api,
        setup_guide=dynamic_setup
    )

