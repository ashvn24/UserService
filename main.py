from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
import uvicorn
from queueprocessor.consumer import  MPQConsumer
from queueprocessor.queue_config import QueueManager
from routes.base import api_router
import threading

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
    queue_manager = QueueManager(queue_name="task_queue")
    queue_manager.setup_queue()
    return app

app = startApplication()

def process_message(body):
    print(f"Processing: {body}")
    
def start_consumer():
    consumer = MPQConsumer(queue_name="task_queue")
    consumer.consume(callback=process_message)
    
@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
    
if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.APP_PORT, reload=True)