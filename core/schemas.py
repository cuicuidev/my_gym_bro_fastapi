from pydantic import BaseModel

class Exercise(BaseModel):
    name: str
    exercise_type_id: int

class ExerciseType(BaseModel):
    type: str