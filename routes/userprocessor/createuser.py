from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.requests import Request
import db.schemas.userSchema as userSchema
import utils.helperfunc as helperfunc
from classes import userprocessor


router = APIRouter(prefix= "/colab/v2/userprocessor", tags=["UserProcessor"])

helper = helperfunc.Helper()

@router.post("/createuser/")
async def create_user(
    data: userSchema.UserSchema, 
    db: Session = Depends(get_db)
):
    
    helper.validator(data)
    processor = userprocessor.UserProcessor(db)
    return await processor.create_user(data)

