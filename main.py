from fastapi import FastAPI, Depends, HTTPException, status, Response

from schemas import Set

from database import Set as DBSet, delete_set_, delete_set_hard_, read_set, create_set, update_set
from database import get_db
from sqlalchemy.orm import Session

from auth import get_user_id_from_token, oauth2_scheme, router

app = FastAPI()

app.include_router(router=router)

@app.get('/')
async def root():
    return "Hello World!"

############################################################## SET ENTRIES ##############################################################

@app.get('/get_set/{id}')
async def get_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    db_set = read_set(db=db, id=id)

    if db_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if db_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

    return db_set

@app.post('/post_set/')
async def post_set(set: Set, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):    
    user_id = get_user_id_from_token(token)
    db_set = create_set(db, set, user_id)
    return db_set

@app.put('/put_set/{id}')
async def put_set(id: int, updated_set: Set, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    existing_set = read_set(db=db, id=id)

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    return update_set(db=db, existing_set=existing_set, updated_set=updated_set)

@app.delete('/delete_set/{id}')
async def delete_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    existing_set = read_set(db=db, id=id)

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    return delete_set_(db=db, existing_set=existing_set)

@app.delete('/delete_set/{id}/hard')
async def hard_delete_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    existing_set = read_set(db=db, id=id)

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    delete_set_hard_(db=db, existing_set=existing_set)
    return Response(status_code=status.HTTP_200_OK, content="DELETED SUCCESSFULLY")


############################################################## SOMETHING ELSE ##############################################################
