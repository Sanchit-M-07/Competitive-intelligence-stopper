from sqlmodel import Session
from app.models import Change
from typing import Dict, Any
import datetime

def generate_insight(change: Change, session: Session) -> Dict[str, Any]:
    """
    Placeholder for LLM insight generation.
    In reality, this would:
    1. Take the change details (summary, change type, etc.)
    2. Prompt an LLM (like Phi-2) to generate a summary, impact score, and suggested action
    3. Return the results

    For now, we return mock data.
    """
    # Mock: generate a summary based on change type
    summary = f"Change in {change.change_type}: {change.summary}"

    # Impact score might be stored already, but we can adjust or keep
    impact_score = change.impact_score if change.impact_score > 0 else 5  # default to 5 if not set

    # Suggested action based on impact score
    if impact_score >= 8:
        suggested_action = "Immediate action required: investigate and respond"
    elif impact_score >= 5:
        suggested_action = "Monitor closely and consider strategic response"
    else:
        suggested_action = "Monitor for further developments"

    return {
        "summary": summary,
        "impact_score": impact_score,
        "suggested_action": suggested_action,
        "created_at": datetime.datetime.utcnow()
    }