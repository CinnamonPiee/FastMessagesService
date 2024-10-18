from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserInDB(UserCreate):
    hashed_password: str


class User(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
