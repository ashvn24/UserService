from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
import db.models as models
import db.schemas.userSchema as userSchema
from classes.authentication import Auth

router = APIRouter(prefix= "/colab/v2/auth", tags=["Auth"])

@router.post("/")
async def auth_call(
    data: userSchema.UserSchema,
    db: Session = Depends(get_db)
):
    auth = Auth(db)
    return await auth.signin(data)