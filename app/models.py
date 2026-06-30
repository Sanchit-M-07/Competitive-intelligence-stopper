from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Competitor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    url: str = Field(index=True)
    label: str = Field(default="competitor")
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Scrape(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    competitor_id: int = Field(foreign_key="competitor.id")
    url: str
    raw_html: str
    cleaned_text: str
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

class Change(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scrape_id: int = Field(foreign_key="scrape.id")
    competitor_id: int = Field(foreign_key="competitor.id")
    change_type: str  # e.g., pricing, product, hiring, content, leadership, other
    similarity_score: float  # cosine similarity distance (lower means more similar)
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    summary: str
    impact_score: int = Field(default=1, ge=1, le=10)
    suggested_action: str

class Insight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    change_id: int = Field(foreign_key="change.id")
    summary: str
    impact_score: int = Field(ge=1, le=10)
    suggested_action: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Card(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    competitor_id: int = Field(foreign_key="competitor.id")
    change_id: int = Field(foreign_key="change.id")
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    archived: bool = Field(default=False)

class CrmRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    change_id: int = Field(foreign_key="change.id")
    crm_id: str  # ID from the external CRM (Notion page ID, Airtable record ID, etc.)
    crm_type: str  # notion, airtable, etc.
    synced_at: datetime = Field(default_factory=datetime.utcnow)
    success: bool = Field(default=False)
    error_message: Optional[str] = None
class SmptSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    smtp_server: str = Field(default="localhost")
    smtp_port: int = Field(default=587)
