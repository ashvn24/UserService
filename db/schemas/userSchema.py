from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = None