from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from pydantic import BaseModel
from app.init_db import get_session
from app.models import Change, Insight, SmptSettings  # We'll create SmptSettings if needed, but for now placeholder
from app.digest.digest import generate_digest, send_digest  # We'll create this
from typing import List, Optional
import datetime

router = APIRouter()

class DigestRequest(BaseModel):
    frequency: str = "daily"  # daily or weekly
    competitor_ids: Optional[List[int]] = None
    min_impact: int = 1

class DigestResponse(BaseModel):
    id: str
    frequency: str
    generated_at: str
    recipient_count: int
    preview: str

@router.post("/generate/", response_model=DigestResponse)
def generate_digest_endpoint(request: DigestRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    # Generate digest in background
    digest_id = f"digest_{datetime.datetime.utcnow().timestamp()}"
    background_tasks.add_task(generate_digest, digest_id, request.frequency, request.competitor_ids, request.min_impact, session)
    return DigestResponse(
        id=digest_id,
        frequency=request.frequency,
        generated_at=datetime.datetime.utcnow().isoformat(),
        recipient_count=0,  # Will be updated by background task
        preview="Digest generation started..."
    )

@router.post("/send/{digest_id}")
def send_digest_endpoint(digest_id: str, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    background_tasks.add_task(send_digest, digest_id, session)
    return {"status": "sending", "digest_id": digest_id}

@router.get("/history/")
def get_digest_history(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    # Placeholder: we don't have a Digest model yet, so return empty list
    return []

@router.get("/templates/")
def get_email_templates():
    return {
        "daily": "Daily competitor intelligence digest",
        "weekly": "Weekly competitor intelligence summary"
    }