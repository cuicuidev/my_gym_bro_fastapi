from pydantic import BaseModel

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