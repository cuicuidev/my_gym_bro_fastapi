# modules
import os, sys

from datetime import datetime, timedelta
from typing import Annotated

# database
from sqlalchemy.orm import Session
from core.database import get_db

# security
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

# api
from fastapi import Depends, HTTPException
from starlette import status

from . import schemas
from . import database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "../app/.env"))
print(BASE_DIR)
sys.path.append(BASE_DIR)

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")

def verify_password(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):

    if len(username) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty username", headers={"WWW-Authenticate" : "Bearer"})
    if len(password) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty password", headers={"WWW-Authenticate" : "Bearer"})
    
    user = database.get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username", headers={"WWW-Authenticate" : "Bearer"})
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password", headers={"WWW-Authenticate" : "Bearer"})
    
    return user

def create_token(data: dict, time_to_expire: datetime | None = None):
    data_dict = data
    if time_to_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_to_expire
    
    data_dict.update({"exp": expires})
    token = jwt.encode(data_dict, key=SECRET_KEY, algorithm=ALGORITHM)
    return token
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="null username", headers={"WWW-Authenticate" : "Bearer"})
    except JWTError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err, headers={"WWW-Authenticate" : "Bearer"})
    
    user = database.get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found", headers={"WWW-Authenticate" : "Bearer"})
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if ~current_user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="inactive user")
    return current_user

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err, headers={"WWW-Authenticate" : "Bearer"})

def get_user_id_from_token(token: str) -> int:
    payload = verify_token(token)
    return payload['user_id']