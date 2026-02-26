# Keeping everything in one file for now
# If the project will be bigger in the future, I will move routes and db logic to separate modules

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.models import Note, NoteCreate, NoteUpdate

logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
# Initialize database on startup so the app is immediately usable
# This avoids manual setup steps and makes testing easier


app = FastAPI(
    title="systems-thinking-project",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"], summary="Healthcheck")
def health():
    return {"ok": True, "degraded": False}
# Health endpoint used for monitoring and automated checks
# Degraded flag will be needed when simulating DB failures


@app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    note = Note(**payload.model_dump())

    session.add(note)
    session.commit()
    session.refresh(note)  # refresh ensures id and latest state are available

    logger.info("note created id=%s", note.id)
    return note
# Create and persist a new note
# SQLite autogenerates primary key on commit


@app.get("/notes", response_model=list[Note])
def list_notes(
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    q = select(Note).order_by(Note.id.desc()).offset(offset).limit(limit)
    return session.exec(q).all()
# Using limit/offset pagination to prevent loading everything into memory
# Sorting by id DESC makes newest entries appear first


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return note
# In SQLite, direct primary key lookup is effective
# By returning 404, API behavior for missing data is kept comnsistent


@app.patch("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(note, key, value)

    session.commit()
    session.refresh(note)

    logger.info("note updated id=%s", note.id)
    return note
# To allow partial updates patch chosen instead of put
# Exclude_unset makes sure that only fields that are provided are modified


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")

    session.delete(note)
    session.commit()

    logger.info("note deleted id=%s", note_id)
    return
# Explicit delete keeps database state consistent
# Returning 204 - successful deletion without response body