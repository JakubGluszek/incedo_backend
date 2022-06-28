from sqlalchemy.orm import Session

from app import crud, schemas


def remove_notebook(db: Session, *, notebook_id: int, user: schemas.User) -> None:
    notebook = crud.notebook.get_by_id_and_user(db, id=notebook_id, user=user)
    crud.note.remove_multi_by_notebook_id(db, notebook_id=notebook.id)
    crud.notebook.remove(db, id=notebook.id, user=user)
    return
