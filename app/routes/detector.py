from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.init_db import get_session
from app.models import Change, Scrape
from app.detector.detector import detect_changes  # We'll create this
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class ChangeDetectionRequest(BaseModel):
    scrape_id: int
    threshold: float = 0.7  # cosine distance threshold (lower means more similar)

class ChangeDetectionResponse(BaseModel):
    scrape_id: int
    similarity_score: float
    is_change: bool
    change_type: str
    change_id: Optional[int] = None

@router.post("/detect/", response_model=ChangeDetectionResponse)
def detect_change(request: ChangeDetectionRequest, session: Session = Depends(get_session)):
    scrape = session.get(Scrape, request.scrape_id)
    if not scrape:
        raise HTTPException(status_code=404, detail="Scrape not found")

    # Call the detection function
    result = detect_changes(scrape, request.threshold, session)

    # If a change was detected and we want to store it
    if result["is_change"] and result["change_id"] is None:
        # Create a change record
        change = Change(
            scrape_id=scrape.id,
            competitor_id=scrape.competitor_id,
            change_type=result["change_type"],
            similarity_score=result["similarity_score"],
            detected_at=result["detected_at"],
            summary=result["summary"],
            impact_score=result["impact_score"],
            suggested_action=result["suggested_action"]
        )
        session.add(change)
        session.commit()
        session.refresh(change)
        result["change_id"] = change.id

    return result

@router.get("/changes/", response_model=List[dict])
def get_changes(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    changes = session.query(Change).offset(skip).limit(limit).all()
    return changes