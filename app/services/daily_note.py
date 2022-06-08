from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas


def create_daily_note(
    db: Session, *, note_in: schemas.DailyNoteCreate, user: schemas.User
) -> schemas.DailyNote:
    # define today's date based on utcnow + user's timezone differance
    if user.settings.time_diff:
        date = datetime.utcnow() + timedelta(hours=user.settings.time_diff)
    else:
        date = datetime.utcnow()

    # check if a note with today's date already exist
    # if it does, raise exception
    if crud.daily_note.get_by_date(db, date=date, user=user):
        raise HTTPException(status_code=400)
    # create & return note
    note = crud.daily_note.create(db, note_in=note_in, user=user)
    return note


def update_daily_note(
    db: Session, *, update: schemas.DailyNoteUpdate, user: schemas.User
) -> schemas.DailyNote:
    # define today's date on utcnow + user's timezone differance
    if user.settings.time_diff:
        date = datetime.utcnow() + timedelta(hours=user.settings.time_diff)
    else:
        date = datetime.utcnow()
    # check if a note with today's date already exist
    # if it does not, raise exception
    note = crud.daily_note.get_by_date(db, date=date, user=user)
    if not note:
        raise HTTPException(status_code=400)
    # update & return note
    note = crud.daily_note.update(db, db_obj=note, obj_in=update)
    return note
