from sqlalchemy.orm import Session

from app import crud, schemas


def create_daily_note(
    db: Session, *, note_in: schemas.DailyNoteCreate, user: schemas.User
) -> schemas.DailyNote:
    # define today's date based on utcnow + user's timezone differance
    # check if a note with today's date already exist
    # if it does, raise exception
    # create & return note
    return


def update_daily_note(
    db: Session, *, update: schemas.DailyNoteUpdate, user: schemas.User
) -> schemas.DailyNote:
    # define today's date on utcnow + user's timezone differance
    # check if a note with today's date already exist
    # if it does not, raise exception
    # update & return note
    return
