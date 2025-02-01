from datetime import datetime, timedelta
from typing import Optional

from fastapi import Header
from core.config import settings
import db.models as models
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from classes.userprocessor import UserProcessor
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from pytz import utc


class Auth(UserProcessor):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db
        
    async def signin(self, data: models.User):
        user = await self.get_user(filterby = "email",value = data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.helper.verify_password(data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")
        authToken, refreshToken = self.create_tokens(user)
        headers = {
            "Authorization": authToken,
            "Refresh-Token": refreshToken,
        }
        return JSONResponse(content={"message": "User signed in successfully"}, headers=headers)
    
    def create_tokens(self, user):
        data = {"id": user.id, "role": user.role}
        to_encode = data.copy()
        expires = datetime.now(utc) + timedelta(minutes=60)
        to_encode.update({"exp": expires})
        authToken = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
        
        refresh_data = {"id": user.id, "role": user.role}
        refresh_encode = refresh_data.copy()
        refresh_expires = datetime.now(utc) + timedelta(days=7)
        refresh_encode.update({"exp": refresh_expires})
        refreshToken = jwt.encode(refresh_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
        
        return authToken, refreshToken
    
    async def refresh_token(self, token):
        user = await self.get_user(filterby="id", value=token["id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        authToken, refreshToken = self.create_tokens(user)
        headers = {
            "Authorization": authToken,
            "Refresh-Token": refreshToken,
        }
        return JSONResponse(content={"message": "Token refreshed successfully"}, headers=headers)
    
def decode(authorization: Optional[str] = Header(None)):
    try:
        payload = jwt.decode(authorization, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError: 
        raise HTTPException(status_code=401, detail="Invalid token")