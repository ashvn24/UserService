from typing import Optional
from pydantic import BaseModel
from ..models import models

class UserSchema(BaseModel):
    username: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = None
    
class UserUpdateSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None