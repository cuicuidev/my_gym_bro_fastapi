from sqlalchemy.orm import Session
from core.database import User as DBUser
from . import schemas

def get_user(db: Session, username: str):
    db_user = db.query(DBUser).filter(DBUser.username == username).first()
    if db_user is None:
        return False
    user_data = {
        "id" : db_user.id,
        "username" : db_user.username,
        "email" : db_user.email,
        "full_name" : db_user.full_name,
        "active" : db_user.active,
        "password" : db_user.password
    }
    user = schemas.UserInDB(**user_data)
    return user
    