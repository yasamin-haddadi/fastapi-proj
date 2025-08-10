from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = Field(default=None, max_length=100)
    role_id: Optional[int] = None
    is_active: bool = True


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=128)
    role_id: Optional[int] = Field(default=2)

class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponseSchema(UserBaseSchema):
    id: UUID

    class Config:
        from_attributes = True
        #exclude_none = True

class PaginatedUsers(BaseModel):
    total: int
    page: int
    size: int
    users: List[UserResponseSchema]