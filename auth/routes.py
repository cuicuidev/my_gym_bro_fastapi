from datetime import timedelta

# database
from sqlalchemy.orm import Session
from core.database import User as DBUser
from core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

# api
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

# schemas
from . import schemas
from . import core

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/token")
async def access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = core.authenticate_user(db, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=core.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = core.create_access_token({"username" : user.username, "user_id" : user.id}, access_token_expires)

    refresh_token_expires = timedelta(days=core.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = core.create_refresh_token(refresh_token_expires)

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }

@router.post("/refresh")
async def refresh_token(data: dict, db: Session = Depends(get_db)):
    refresh_token = data['refresh_token']
    access_token = data['access_token']

@router.post("/signup/")
async def signup(form_data: schemas.SignUpForm, db: Session = Depends(get_db)):
    username = form_data.username
    email = form_data.email
    password = form_data.password
    confirm_password = form_data.confirm_password
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords don't match", headers={"WWW-Authenticate" : "Bearer"})
    full_name = form_data.full_name
    active = True

    hashed_password = core.pwd_content.encrypt(password)
    db_user = DBUser(username = username, email = email, password = hashed_password, full_name = full_name, active = active)
    db.add(db_user)
    db.commit()