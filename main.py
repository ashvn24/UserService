from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
import uvicorn
from routes.base import api_router

def include_router(app: FastAPI):
    app.include_router(api_router)

def startApplication():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Content-Disposition", "Content-Type", "Authorization"],
    )
    include_router(app)
    return app

app = startApplication()

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.APP_PORT, reload=True)