# Pydantic/SQLModel models
# Goal: keep schemas simple and predictable for CRUD + tests

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    # Base fields shared by DB model + input schemas
    title: str
    body: str


class Note(NoteBase, table=True):
    # Table model: stored in SQLite
    id: Optional[int] = Field(default=None, primary_key=True)

    # Store timestamps in UTC to avoid timezone troubles
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NoteCreate(NoteBase):
    # Post /notes uses the same fields as NoteBase
    pass


class NoteUpdate(SQLModel):
    # Patch schema: all fields optional (only provided ones are updated)
    title: Optional[str] = None
    body: Optional[str] = None