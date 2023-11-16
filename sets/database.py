from core import database
from . import schemas
from sqlalchemy.orm import Session

def create_set(db: Session, set_data: schemas.Set, user_id: int):
    db_set = database.Set(**set_data.model_dump(), user_id=user_id, active=True)
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

def read_set(db: Session, id: int):
    return db.query(database.Set).filter(database.Set.id == id).first()

def update_set(db: Session, existing_set: database.Set, updated_set: schemas.Set):
    for key, value in updated_set.model_dump().items():
        setattr(existing_set, key, value)

    db.commit()
    db.refresh(existing_set)
    return existing_set

def delete_set_(db: Session, existing_set: database.Set):
    existing_set.active = False
    db.commit()
    db.refresh(existing_set)
    return existing_set

def delete_set_hard_(db: Session, existing_set: database.Set):
    db.delete(existing_set)
    db.commit()

def activate_set(db: Session, existing_set: database.Set):
    existing_set.active = True
    db.commit()
    db.refresh(existing_set)
    return existing_set

def read_sets_by_user_id(db: Session, user_id: int):
    return db.query(database.Set).filter(database.Set.user_id == user_id).all()