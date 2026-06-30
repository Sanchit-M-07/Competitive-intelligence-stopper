from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from app.init_db import get_session
from app.models import Competitor, Scrape
from app.scraper.scraper import scrape_sync  # Use the sync version
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class CompetitorCreate(BaseModel):
    name: str
    url: str
    label: str = "competitor"

class CompetitorRead(CompetitorCreate):
    id: int
    active: bool
    created_at: datetime
    updated_at: datetime

@router.post("/competitors/", response_model=CompetitorRead)
def create_competitor(competitor: CompetitorCreate, session: Session = Depends(get_session)):
    db_competitor = Competitor.from_orm(competitor)
    session.add(db_competitor)
    session.commit()
    session.refresh(db_competitor)
    return db_competitor

@router.get("/competitors/", response_model=List[CompetitorRead])
def read_competitors(session: Session = Depends(get_session)):
    competitors = session.query(Competitor).filter(Competitor.active == True).all()
    return competitors

@router.post("/scrape/{competitor_id}")
def trigger_scrape(competitor_id: int, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    competitor = session.get(Competitor, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    # Run scrape in background
    background_tasks.add_task(scrape_sync, competitor_id)
    return {"message": "Scraping started in background"}

@router.get("/scrapes/{competitor_id}")
def get_scrapes(competitor_id: int, session: Session = Depends(get_session)):
    scraps = session.query(Scrape).filter(Scrape.competitor_id == competitor_id).order_by(Scrape.scraped_at.desc()).all()
    return scraps