from pydantic import BaseModel

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