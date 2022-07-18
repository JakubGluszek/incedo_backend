from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_id_and_user_id(self, db: Session, *, id: int, user_id: int) -> ModelType:
        """
        Throws 404 if model not found or model.user_id != user_id
        """
        db_obj = (
            db.query(self.model)
            .filter(self.model.id == id, self.model.user_id == user_id)
            .first()
        )
        if not db_obj:
            raise HTTPException(status_code=404)
        return db_obj

    def remove_multi(
        self, db: Session, *, objects_ids: List[int], user_id: int
    ) -> None:
        objects = (
            db.query(self.model)
            .filter(self.model.id.in_(objects_ids), self.model.user_id == user_id)
            .all()
        )
        for obj in objects:
            db.delete(obj)
        db.commit()
        return

    def get_multi(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_first_by_user_id(self, db: Session, *, user_id: int) -> None:
        obj = db.query(self.model).filter(self.model.user_id == user_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return

    def remove_all_by_user_id(self, db: Session, *, user_id: int) -> None:
        objects = db.query(self.model).filter(self.model.user_id == user_id).all()
        for obj in objects:
            db.delete(obj)
        db.commit()
        return
