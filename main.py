import uvicorn
import os, sys
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Set as SchemaSet
from schema import User as SchemaUser

from models import Set as ModelSet
from models import User as ModelUser

app = FastAPI()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "./app/.env"))
sys.path.append(BASE_DIR)

app.add_middleware(DBSessionMiddleware, db_url = os.environ["POSTGRES_URL"])

@app.get('/')
async def root():
    return "Hello World!"

@app.post('/post_set/', response_model=SchemaSet)
async def post_set(set: SchemaSet) -> SchemaSet:
    unix_timestamp_ms = set.unix_timestamp_ms
    weight_kg = set.weight_kg
    n_repetitions = set.n_repetitions
    rir = set.rir
    duration_ms = set.duration_ms
    tir_ms = set.tir_ms
    user_id = set.user_id
    exercise_id = set.exercise_id
    previous_set_id = set.previous_set_id
    next_set_id = set.next_set_id
    active = True
    
    db_set = ModelSet(
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

    db.session.add(db_set)
    db.session.commit()

    return db_set

@app.post('/sign_up/', response_model=SchemaUser)
async def sign_up(user: SchemaUser) -> SchemaUser:
    username = user.username
    email = user.email
    active = True

    db_user = ModelUser(
        username = username,
        email = email,
        active = active
    )

    db.session.add(db_user)
    db.session.commit()

    return db_user