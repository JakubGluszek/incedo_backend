from typing import List
from sqlalchemy.orm import Session

from app import schemas, crud, models


class NotesServices:
    """
    Handles operations around notes beyond CRUD methods.
    """

    def sort(self, db: Session, *, payload: schemas.NewRank, user_id: int) -> bool:
        """
        Handle's manual sorting by user.

        Given a valid payload the function will update all necessary models ranks.
        """
        # note.parent_id == 0 means that it's deleted, which is why this can't happen here
        if payload.type == "note" and payload.parent_id == 0:
            return False

        # get object that is being pushed to a new rank position
        if payload.type == "note":
            obj = crud.note.get_by_id_and_user_id(db, id=payload.id, user_id=user_id)
        elif payload.type == "folder":
            obj = crud.note_folder.get_by_id_and_user_id(
                db, id=payload.id, user_id=user_id
            )
        else:
            return False

        # get siblings
        siblings: List[schemas.Note, schemas.NoteFolder] = []

        siblings += (
            db.query(models.NoteFolder)
            .filter(
                models.NoteFolder.user_id == user_id,
                models.NoteFolder.parent_id == payload.parent_id,
            )
            .all()
        )

        if payload.parent_id != 0:
            siblings += (
                db.query(models.Note)
                .filter(
                    models.Note.user_id == user_id,
                    models.Note.parent_id == payload.parent_id,
                )
                .all()
            )

        print(siblings)
        # sort obj & siblings
        for s in siblings:
            print('id, rank')
            print(s.id, s.rank)
            if obj.rank > payload.rank:
                print('bigger or equal')
                if s.rank >= payload.rank:
                    s.rank += 1
                    print('+1')
                    db.add(s)
            elif obj.rank < payload.rank:
                if s.rank <= payload.rank and s.rank > obj.rank:
                    s.rank -= 1
                    print('-1')
                    db.add(s)
            print('done')
        
        if payload.parent_id:
            obj.parent_id = payload.parent_id
        obj.rank = payload.rank
        
        print('obj new rank', payload.rank)
        db.add(obj)
        db.commit()

        return True


notes = NotesServices()
