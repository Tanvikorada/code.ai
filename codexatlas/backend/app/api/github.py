from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.database import get_db
from app.models.orm import ScanResult, User
from app.core.dependencies import get_current_user
from app.services import process_repository

router = APIRouter()

class ScanRequest(BaseModel):
    url: str

class ScanResponse(BaseModel):
    id: str
    status: str
    message: str

class StatusResponse(BaseModel):
    id: str
    status: str
    url: str
    created_at: str

@router.post("/scan", response_model=ScanResponse)
async def scan_repository(
    request: ScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Scan a GitHub repository using Celery for background processing"""
    from app.worker import process_repository_task
    
    repo_id = str(uuid.uuid4())
    
    # Create the initial record in DB
    new_scan = ScanResult(
        id=repo_id,
        user_id=current_user.id,
        repo_url=request.url,
        status="processing"
    )
    db.add(new_scan)
    db.commit()
    
    # Spawn background task via Celery
    process_repository_task.delay(repo_id, request.url)
    
    return ScanResponse(
        id=repo_id,
        status="processing",
        message="Repository scan started in the background."
    )

@router.get("/status/{repo_id}", response_model=StatusResponse)
async def get_status(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check the status of a repository scan"""
    scan = db.query(ScanResult).filter(ScanResult.id == repo_id, ScanResult.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    return StatusResponse(
        id=scan.id,
        status=scan.status,
        url=scan.repo_url,
        created_at=scan.created_at.isoformat()
    )

@router.get("/result/{repo_id}")
async def get_result(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the full result data of a completed repository scan"""
    scan = db.query(ScanResult).filter(ScanResult.id == repo_id, ScanResult.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    if scan.status != "completed":
        raise HTTPException(status_code=400, detail="Scan is not completed yet")
        
    if not scan.data:
        raise HTTPException(status_code=404, detail="Scan data is missing")
        
    return scan.data
