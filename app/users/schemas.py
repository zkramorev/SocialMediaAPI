from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    user_name: Optional[str] = None