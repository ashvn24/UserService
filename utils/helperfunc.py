
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

class Helper:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self,password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    @property
    def userdata(self):
        return ['two-factor', 'updated_at', 'password', 'otp', 'created_at']
    
    @staticmethod
    def validator(data):
        data = data.model_dump()
        for item, val in data.items():
            if val == "":
                return JSONResponse(content={"message": f"{item} cannot be empty"}, status_code=400)
            
    def clean_data(self, data, type):
        if type == 'userdata':
            exclude = set(self.userdata)  

        if isinstance(data, list):
            return [{key: value for key, value in item.__dict__.items() if key not in exclude} for item in data]
        if hasattr(data, "__dict__"):
            data = data.__dict__
        if not isinstance(data, dict): 
            raise ValueError("Expected a dictionary, object, or list of dictionaries/objects")
        return {key: value for key, value in data.items() if key not in exclude}

