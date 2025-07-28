from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.pokerfish.core.manager import ConnectionManager
from src.pokerfish.routes.websocket import router as websocket_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

app.include_router(websocket_router)
    
