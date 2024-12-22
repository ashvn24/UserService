
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

class Helper:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self,password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validator(data):
        data = data.model_dump()
        for item, val in data.items():
            if val == "":
                return JSONResponse(content={"message": f"{item} cannot be empty"}, status_code=400)
            
