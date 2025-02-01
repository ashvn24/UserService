from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fastapi.requests import Request
import db.schemas.userSchema as userSchema
import utils.helperfunc as helperfunc
from classes import userprocessor


router = APIRouter(prefix= "/colab/v2/userprocessor", tags=["UserProcessor"])

helper = helperfunc.Helper()

@router.post("/create-user/")
async def create_user(
    data: userSchema.UserSchema, 
    db: Session = Depends(get_db)
):
    helper.validator(data)
    processor = userprocessor.UserProcessor(db)
    return await processor.create_user(data)

@router.post('/update-user/')
async def update_user(
    data: userSchema.UserUpdateSchema,
    id: int,
    db: Session = Depends(get_db)
):
    processor = userprocessor.UserProcessor(db)
    return await processor.update_user(data, id)

@router.get('/get-users/')
async def get_users(
    db: Session = Depends(get_db)
):
    processor = userprocessor.UserProcessor(db)
    result = await processor.get_user()
    if result:
        return helper.clean_data(result, "userdata")
    
