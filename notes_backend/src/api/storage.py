from typing import List, Optional
from uuid import UUID, uuid4
from dotenv import load_dotenv

from .models import Note, NoteCreate, NoteUpdate

# Load .env for future file/db config needs
load_dotenv()

class InMemoryNoteStorage:
    """
    In-memory storage for notes. This class manages all CRUD operations.
    Swap this class for a persistent backend (file/db) as needed.
    """
    def __init__(self):
        self._notes = {}

    # PUBLIC_INTERFACE
    def create_note(self, note_create: NoteCreate) -> Note:
        """Create a new note and assign a UUID."""
        note_id = uuid4()
        note = Note(id=note_id, **note_create.model_dump())
        self._notes[note_id] = note
        return note

    # PUBLIC_INTERFACE
    def get_note(self, note_id: UUID) -> Optional[Note]:
        """Retrieve a note by its ID."""
        return self._notes.get(note_id)

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[Note]:
        """List all available notes."""
        return list(self._notes.values())

    # PUBLIC_INTERFACE
    def update_note(self, note_id: UUID, note_update: NoteUpdate) -> Optional[Note]:
        """Update an existing note with new values."""
        note = self._notes.get(note_id)
        if not note:
            return None
        updated_data = note.model_dump()
        update_fields = note_update.model_dump(exclude_unset=True)
        updated_data.update(update_fields)
        updated_note = Note(**updated_data)
        self._notes[note_id] = updated_note
        return updated_note

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: UUID) -> bool:
        """Delete a note by its ID. Returns True if deleted, False if note not found."""
        return self._notes.pop(note_id, None) is not None

# Singleton instance for app-wide use
note_storage = InMemoryNoteStorage()
