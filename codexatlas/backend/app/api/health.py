from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.orm import ScanResult, User
from app.core.dependencies import get_current_user
router = APIRouter()

@router.get("/{repo_id}")
async def get_health(
    repo_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the health analysis for a repository"""
    scan = db.query(ScanResult).filter(ScanResult.id == repo_id, ScanResult.user_id == current_user.id).first()
    if not scan or scan.status != "completed" or not scan.data:
        raise HTTPException(status_code=404, detail="Health data not found or scan not completed")
    
    return scan.data.get("health", {})
