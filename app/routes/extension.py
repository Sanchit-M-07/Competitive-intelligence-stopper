from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from pydantic import BaseModel
from app.init_db import get_session
from app.models import Competitor
from app.extension.extension import register_competitor  # We'll create this
from typing import Optional
from datetime import datetime

router = APIRouter()

API_KEY_HEADER = "X-API-Key"

class ExtensionConfig(BaseModel):
    url: str
    competitor_label: str
    section_selector: str = "body"
    check_interval_hours: int = 6

class ExtensionConfigResponse(ExtensionConfig):
    id: int
    created_at: datetime
    is_active: bool

@router.post("/register/", response_model=ExtensionConfigResponse)
def register_competitor_endpoint(
    config: ExtensionConfig,
    x_api_key: str = Header(None),
    session: Session = Depends(get_session)
):
    # Validate API key (in production, use proper auth)
    if x_api_key != "dev-key-123":  # In reality, use a secure method
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Register the competitor
    competitor = register_competitor(config.url, config.competitor_label, session)
    if not competitor:
        raise HTTPException(status_code=400, detail="Failed to register competitor")

    return ExtensionConfigResponse(
        id=competitor.id,
        url=competitor.url,
        competitor_label=competitor.label,
        section_selector=config.section_selector,
        check_interval_hours=config.check_interval_hours,
        created_at=competitor.created_at,
        is_active=competitor.active
    )

@router.get("/competitors/", response_model=list)
def get_registered_competitors(session: Session = Depends(get_session)):
    competitors = session.query(Competitor).filter(Competitor.active == True).all()
    return competitors

@router.get("/health/")
def extension_health():
    return {"status": "placeholder", "service": "Chrome extension integration"}