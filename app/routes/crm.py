from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from pydantic import BaseModel
from app.init_db import get_session
from app.models import Change, CrmRecord
from app.crm.crm import sync_to_crm  # We'll create this
from typing import List, Optional

router = APIRouter()

class CrmSyncRequest(BaseModel):
    change_id: int
    crm_type: str = "notion"  # notion, airtable, etc.

class CrmSyncResponse(BaseModel):
    change_id: int
    crm_id: str
    crm_type: str
    synced_at: str
    success: bool
    error_message: Optional[str] = None

@router.post("/sync/", response_model=CrmSyncResponse)
def sync_change_to_crm(request: CrmSyncRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    change = session.get(Change, request.change_id)
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")

    # Sync to CRM in background
    background_tasks.add_task(sync_to_crm, change.id, request.crm_type, session)
    return CrmSyncResponse(
        change_id=change.id,
        crm_id="pending",  # Will be updated by background task
        crm_type=request.crm_type,
        synced_at="pending",
        success=False,
        error_message="Sync in progress"
    )

@router.get("/records/")
def get_crm_records(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    records = session.query(CrmRecord).offset(skip).limit(limit).all()
    return records

@router.get("/health/")
def crm_health():
    return {"status": "placeholder", "service": "CRM sync"}