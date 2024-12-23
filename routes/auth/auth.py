from typing import Annotated, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
import db.models as models
import db.schemas.userSchema as userSchema
from classes.authentication import Auth, decode

router = APIRouter(prefix= "/colab/v2/auth", tags=["Auth"])


@router.post("/")
async def auth_call(
    data: userSchema.UserSchema,
    db: Session = Depends(get_db)
):
    auth = Auth(db)
    return await auth.signin(data)

@router.post("/token-refresh/")
async def token_refresh(
    db: Session = Depends(get_db),
    token: Dict = Depends(decode),
):
    auth = Auth(db)
    return await auth.refresh_token(token)