from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from uuid import UUID

from .models import Note, NoteCreate, NoteUpdate
from .storage import note_storage

app = FastAPI(
    title="Notes API",
    description="A simple notes application backend providing CRUD operations using FastAPI.",
    version="1.0.0",
    openapi_tags=[
        {"name": "notes", "description": "Operations with notes (create, read, update, delete)"},
        {"name": "health", "description": "Health check"}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Health check endpoint to verify service status."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.post(
    "/notes/",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    tags=["notes"],
    responses={
        201: {"description": "Note created successfully"},
        400: {"description": "Validation error"}
    }
)
def create_note(note_create: NoteCreate):
    """
    Create a new note with a unique ID.

    - **title**: Title of the note
    - **content**: Body/content of the note
    """
    note = note_storage.create_note(note_create)
    return note

# PUBLIC_INTERFACE
@app.get(
    "/notes/",
    response_model=List[Note],
    summary="List all notes",
    tags=["notes"],
    responses={200: {"description": "List of all notes"}}
)
def list_notes():
    """
    Return a list of all notes.
    """
    return note_storage.list_notes()

# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    summary="Get a note by ID",
    tags=["notes"],
    responses={
        200: {"description": "The note with the given ID"},
        404: {"description": "Note not found"}
    }
)
def get_note(note_id: UUID):
    """
    Retrieve a note by its UUID.
    """
    note = note_storage.get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    summary="Update a note",
    tags=["notes"],
    responses={
        200: {"description": "Note updated"},
        404: {"description": "Note not found"}
    }
)
def update_note(note_id: UUID, note_update: NoteUpdate):
    """
    Update an existing note by its UUID.

    - **title**: New (optional) title for the note
    - **content**: New (optional) content for the note
    """
    note = note_storage.update_note(note_id, note_update)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    tags=["notes"],
    responses={
        204: {"description": "Note deleted"},
        404: {"description": "Note not found"}
    }
)
def delete_note(note_id: UUID):
    """
    Delete a note by its UUID.
    """
    deleted = note_storage.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
