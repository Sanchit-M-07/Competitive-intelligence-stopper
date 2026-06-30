from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from app.init_db import get_session
from app.models import Change, Insight
from app.llm.llm import generate_insight

router = APIRouter()

class InsightRequest(BaseModel):
    change_id: int

class InsightResponse(BaseModel):
    change_id: int
    summary: str
    impact_score: int  # 1-10
    suggested_action: str
    insight_id: int

@router.post("/generate/", response_model=InsightResponse)
def create_insight(request: InsightRequest, session: Session = Depends(get_session)):
    change = session.get(Change, request.change_id)
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")

    # Generate insight using LLM
    result = generate_insight(change, session)

    # Save the insight
    insight = Insight(
        change_id=change.id,
        summary=result["summary"],
        impact_score=result["impact_score"],
        suggested_action=result["suggested_action"],
        created_at=result["created_at"]
    )
    session.add(insight)
    session.commit()
    session.refresh(insight)

    return InsightResponse(
        change_id=change.id,
        summary=insight.summary,
        impact_score=insight.impact_score,
        suggested_action=insight.suggested_action,
        insight_id=insight.id
    )

@router.get("/insights/")
def get_insights(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    insights = session.query(Insight).offset(skip).limit(limit).all()
    return insights