import db.models as models
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from classes.userprocessor import UserProcessor
from sqlalchemy.orm import Session

class Auth(UserProcessor):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db
        
    async def signin(self, data: models.User):
        user = self.get_user(filterby = "email",value = data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content={"message": "User signed in successfully"})