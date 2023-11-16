import os, sys
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from database import User as DBUser
from database import get_db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "./app/.env"))
sys.path.append(BASE_DIR)

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    active: bool | None = None

class UserInDB(User):
    password: str

class SignUpForm(User):
    password: str
    confirm_password: str


pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/token/")
async def post_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token({"username" : user.username, "user_id" : user.id}, access_token_expires)
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }

@router.post("/signup/")
async def signup(form_data: SignUpForm, db: Session = Depends(get_db)):
    username = form_data.username
    email = form_data.email
    password = form_data.password
    confirm_password = form_data.confirm_password
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords don't match", headers={"WWW-Authenticate" : "Bearer"})
    full_name = form_data.full_name
    active = True

    hashed_password = pwd_content.encrypt(password)
    db_user = DBUser(username = username, email = email, password = hashed_password, full_name = full_name, active = active)
    db.add(db_user)
    db.commit()


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
    user = UserInDB(**user_data)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):

    if len(username) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty username", headers={"WWW-Authenticate" : "Bearer"})
    if len(password) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="empty password", headers={"WWW-Authenticate" : "Bearer"})
    
    user = get_user(db, username)
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
    
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found", headers={"WWW-Authenticate" : "Bearer"})
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
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