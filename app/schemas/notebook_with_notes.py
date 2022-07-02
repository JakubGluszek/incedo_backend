from typing import List
from .notebook import NotebookOut
from .note import NoteOut


class NotebookWithNotes(NotebookOut):
    notes: List[NoteOut]
    sections: List[NotebookOut]
