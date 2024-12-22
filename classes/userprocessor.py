from typing import Any, Union
import db.models as models
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.helperfunc import Helper

class UserProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.helper = Helper()
    
    def get_user(self, value: Union[int, str] = None, filterby: str = None):
        if filterby and value:
            user = self.db.query(models.User).filter(getattr(models.User, filterby) == value).one_or_none()
        return user
        
    async def create_user(self, data: models.User):
        user = self.get_user(filterby="email", value=data.email)
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        data_dict = data.dict()
        data_dict["password"] = self.helper.hash_password(data_dict["password"])
        data = models.User(**data_dict)
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        
        return self.response( status_code=201, content={"message": "User created successfully"})
    
    async def delete_user(self, user_id: int):
        user = self.get_user(value=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
        return self.response(status_code=200, content={"message": "User deleted successfully"})
    
    def response(self, status_code: int, content: dict):
        return JSONResponse(status_code=status_code, content=content)

    