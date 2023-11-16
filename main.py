from fastapi import FastAPI, Depends, HTTPException, status, Response

from models import Set

from database import Set as DBSet
from database import get_db
from sqlalchemy.orm import Session

from auth import oauth2_scheme, router, verify_token

app = FastAPI()

app.include_router(router=router)

@app.get('/')
async def root():
    return "Hello World!"

############################################################## SET ENTRIES ##############################################################

def get_user_id(token: str) -> int:
    payload = verify_token(token)
    return payload['user_id']


@app.get('/get_set/{id}')
async def get_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id(token)
    db_set = db.query(DBSet).filter(DBSet.id == id).first()

    if db_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if db_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")

    return db_set

@app.post('/post_set/')
async def post_set(set: Set, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    unix_timestamp_ms = set.unix_timestamp_ms
    weight_kg = set.weight_kg
    n_repetitions = set.n_repetitions
    rir = set.rir
    duration_ms = set.duration_ms
    tir_ms = set.tir_ms
    user_id = get_user_id(token)
    exercise_id = set.exercise_id
    previous_set_id = set.previous_set_id
    next_set_id = set.next_set_id
    active = True
    
    db_set = DBSet(
        unix_timestamp_ms = unix_timestamp_ms,
        weight_kg = weight_kg,
        n_repetitions = n_repetitions,
        rir = rir,
        duration_ms = duration_ms,
        tir_ms = tir_ms,
        user_id = user_id,
        exercise_id = exercise_id,
        previous_set_id = previous_set_id,
        next_set_id = next_set_id,
        active = active
    )

    db.add(db_set)
    db.commit()
    return Response(content="CREATED", status_code=status.HTTP_201_CREATED)

@app.put('/put_set/{id}')
async def put_set(id: int, updated_set: Set, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id(token)
    existing_set = db.query(DBSet).filter(DBSet.id == id).first()

    if existing_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if existing_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    existing_set.unix_timestamp_ms = updated_set.unix_timestamp_ms
    existing_set.unix_timestamp_ms = updated_set.unix_timestamp_ms
    existing_set.weight_kg = updated_set.weight_kg
    existing_set.n_repetitions = updated_set.n_repetitions
    existing_set.rir = updated_set.rir
    existing_set.duration_ms = updated_set.duration_ms
    existing_set.tir_ms = updated_set.tir_ms

    existing_set.exercise_id = updated_set.exercise_id
    existing_set.previous_set_id = updated_set.previous_set_id
    existing_set.next_set_id = updated_set.next_set_id

    db.commit()

    return Response(content="UPDATED", status_code=status.HTTP_202_ACCEPTED)

@app.delete('/delete_set/{id}')
async def delete_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id(token)
    db_set = db.query(DBSet).filter(DBSet.id == id).first()

    if db_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if db_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    db_set.active = False

    db.commit()

    return Response(content="DELETED", status_code=status.HTTP_202_ACCEPTED)

@app.delete('/delete_set/{id}/hard')
async def hard_delete_set(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id(token)
    db_set = db.query(DBSet).filter(DBSet.id == id).first()

    if db_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"not found {id=}")
    
    if db_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    
    db.delete(db_set)
    db.commit()

    return Response(content="ERASED", status_code=status.HTTP_202_ACCEPTED)


############################################################## SOMETHING ELSE ##############################################################
