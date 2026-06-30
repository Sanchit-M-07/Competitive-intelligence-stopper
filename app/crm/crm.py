from sqlmodel import Session
from app.models import Change, CrmRecord
from typing import Dict, Any
import datetime
import random

def sync_to_crm(change_id: int, crm_type: str, session: Session) -> Dict[str, Any]:
    """
    Placeholder for syncing a change to an external CRM (Notion, Airtable, etc.).
    In reality, this would:
    1. Fetch the change from the DB
    2. Format the data for the CRM API
    3. Make an HTTP request to the CRM (Notion API, Airtable API, etc.)
    4. Store the CRM's response ID in the CrmRecord table
    5. Handle errors and retries

    For now, we simulate success or failure randomly.
    """
    change = session.get(Change, change_id)
    if not change:
        return {"success": False, "error": "Change not found"}

    # Simulate network delay
    # In a real app, we would use async or a background task properly
    # For this placeholder, we'll just do the work synchronously

    # Simulate success/failure (90% success)
    success = random.random() < 0.9
    crm_id = f"crm_{random.randint(10000, 99999)}" if success else None
    error_message = None if success else "Failed to connect to CRM"

    # Create a CRM record
    crm_record = CrmRecord(
        change_id=change.id,
        crm_id=crm_id or "",
        crm_type=crm_type,
        synced_at=datetime.datetime.utcnow(),
        success=success,
        error_message=error_message
    )
    session.add(crm_record)
    session.commit()
    session.refresh(crm_record)

    return {
        "success": success,
        "crm_id": crm_id,
        "error_message": error_message
    }