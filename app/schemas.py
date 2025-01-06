from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str
    client: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class MovieSchema(BaseModel):
    id: int
    title: str
    director: str
    genre: str
    year: int

    class Config:
        orm_mode = True

# Shared properties for Movie
class MovieBase(BaseModel):
    title: str
    director: str
    genre: str
    year: int

# Properties to receive on Movie creation
class MovieCreate(MovieBase):
    pass

# Properties to return via API
class MovieResponse(MovieBase):
    id: int

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    user_first_name: str
    user_last_name: str
    user_e_mail_id: Optional[str] = None
    user_phone_number: Optional[str] = None
    user_login_id: str
    client_id: int

    class Config:
        orm_mode = True
