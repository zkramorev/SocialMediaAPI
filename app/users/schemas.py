from typing import Optional

from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    user_name: Optional[str] = None
