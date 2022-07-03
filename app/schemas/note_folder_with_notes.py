from typing import List

from .note import NoteOut
from .note_folder import NoteFolderOut


class NoteFolderWithNotes(NoteFolderOut):
    notes: List[NoteOut]
    sections: List[NoteFolderOut]
