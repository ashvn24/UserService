import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "CoLab"
    PROJECT_VERSION: str = "1.2.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    APP_PORT: int = int(os.getenv("PORT"))
    HOST: str = os.getenv("HOST")
    POOL_SIZE: int = int(os.getenv("POOL_SIZE"))
    POOL_TIMEOUT: int = int(os.getenv("POOL_TIMEOUT"))
    POOL_RECYCLE: int = int(os.getenv("POOL_RECYCLE"))
    MAX_OVERFLOW: int = int(os.getenv("MAX_OVERFLOW"))
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    AMPQ_URL: str = os.getenv("AMPQ_URL")
    
settings = Settings()