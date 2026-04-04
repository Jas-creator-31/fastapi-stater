from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class LoginPayload(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(
        from_attributes=True
    )

class UserAgentInfo(BaseModel):
    browser: Optional[str]
    os: Optional[str]
    device: Optional[str]
    is_mobile: Optional[bool]

class TokenServiceReturn(BaseModel):
    sid: str
    access_token: str
    refresh_token: str
    hashed_refresh_token: str