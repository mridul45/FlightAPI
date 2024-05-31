from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    age: int
    password: str


class UserDetail(BaseModel):
    name: str
    email: str


class UpdateUser(BaseModel):
    name: str
    email: str
    age: int