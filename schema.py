from pydantic import BaseModel

class Exercise(BaseModel):
    name: str
    exercise_type_id: int

    class Config:
        orm_mode = True

class ExerciseType(BaseModel):
    type: str

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    email: str

    active: bool

    class Config:
        orm_mode = True

class Set(BaseModel):
    unix_timestamp_ms: float

    weight_kg: float | None
    n_repetitions: int | None
    rir: float | None
    duration_ms: float | None
    tir_ms: float | None

    user_id: int
    exercise_id: int

    previous_set_id: int | None
    next_set_id: int | None

    active: bool

    class Config:
        orm_mode = True