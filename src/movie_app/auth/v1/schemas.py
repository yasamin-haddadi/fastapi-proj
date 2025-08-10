from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: constr(min_length=8) = Field(..., description="User password")


class TokenAccess(BaseModel):
    access_token: str
    refresh_token: str
    # token_type: str = 'bearer'


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    type: Optional[str] = None

#
# class RefreshTokenRequest(BaseModel):
#     refresh_token: str

