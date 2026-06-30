from sqlmodel import Session
from app.models import Competitor
import datetime

def register_competitor(url: str, label: str, session: Session) -> Competitor:
    """
    Register a competitor for monitoring via the Chrome extension.
    In reality, this might also validate the URL, check for duplicates, etc.
    """
    # Check if a competitor with this URL already exists
    existing = session.query(Competitor).filter(Competitor.url == url).first()
    if existing:
        # Update the label if needed
        existing.label = label
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing

    # Create new competitor
    competitor = Competitor(
        url=url,
        label=label,
        name=url,  # Use URL as name for now; could be improved
        active=True
    )
    session.add(competitor)
    session.commit()
    session.refresh(competitor)
    return competitor