from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    pseudo: str = Field(min_length=2, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    pseudo: str | None = Field(default=None, min_length=2, max_length=20)
    email: EmailStr | None = None


class UserOut(BaseModel):
    id: int
    pseudo: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
