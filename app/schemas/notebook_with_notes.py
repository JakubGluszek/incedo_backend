from typing import List

from .note import NoteOut
from .notebook import NotebookOut


class NotebookWithNotes(NotebookOut):
    notes: List[NoteOut]
    sections: List[NotebookOut]
