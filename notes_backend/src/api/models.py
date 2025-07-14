from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base model for a note."""
    title: str = Field(..., description="The title of the note")
    content: str = Field(..., description="The content/body of the note")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Model for creating a note."""
    pass

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Model for updating a note."""
    title: Optional[str] = Field(None, description="The new title for the note")
    content: Optional[str] = Field(None, description="The new content for the note")

# PUBLIC_INTERFACE
class Note(NoteBase):
    """Model returned for a note, including its ID."""
    id: UUID = Field(..., description="Unique identifier for the note")
