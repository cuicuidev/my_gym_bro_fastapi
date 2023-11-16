from pydantic import BaseModel

##################################### AUTH
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserInDB(User):
    id: int
    password: str
    active: bool | None = None

class SignUpForm(User):
    password: str
    confirm_password: str


##################################### CORE
class Exercise(BaseModel):
    name: str
    exercise_type_id: int

class ExerciseType(BaseModel):
    type: str


##################################### USER GENERATED DATA
class Set(BaseModel):
    unix_timestamp_ms: float

    weight_kg: float | None
    n_repetitions: int | None
    rir: float | None
    duration_ms: float | None
    tir_ms: float | None

    exercise_id: int

    previous_set_id: int | None
    next_set_id: int | None