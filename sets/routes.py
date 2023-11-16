from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import core
import auth
from . import database
from . import schemas


router = APIRouter(
    prefix="/sets",
    tags=["sets"],
)

get_db = core.database.get_db
oauth2_scheme = auth.core.oauth2_scheme
get_user_id_from_token = auth.core.get_user_id_from_token

@router.get('/get/{id}')
async def get_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    db_set = database.read_set(db=db, id=id)

    if db_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if db_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

    return db_set

@router.post('/post/')
async def post_set(set: schemas.Set, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):    
    user_id = get_user_id_from_token(token)
    db_set = database.create_set(db, set, user_id)
    return db_set

@router.put('/put/{id}')
async def put_set(id: int, updated_set: schemas.Set, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    existing_set = database.read_set(db=db, id=id)

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    return database.update_set(db=db, existing_set=existing_set, updated_set=updated_set)

@router.delete('/delete/{id}')
async def delete_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    existing_set = database.read_set(db=db, id=id)

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    return database.delete_set_(db=db, existing_set=existing_set)

@router.delete('/delete_hard/{id}')
async def hard_delete_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    existing_set = database.read_set(db=db, id=id)

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    database.delete_set_hard_(db=db, existing_set=existing_set)
    return Response(status_code=status.HTTP_200_OK, content="DELETED SUCCESSFULLY")