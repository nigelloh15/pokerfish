from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.pokerfish.core.manager import ConnectionManager
from src.pokerfish.routes.websocket import router as websocket_router
from src.pokerfish.db.redis import connect_to_redis, close_redis_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

@app.on_event("startup")
def startup_event():
    connect_to_redis()
    print("Connected to Redis")

@app.on_event("shutdown")
def shutdown_event():
    close_redis_connection()
    print("Closed Redis connection")

@app.get("/")
def root():
    return {"message": "Hello, World!"}

app.include_router(websocket_router)
    
