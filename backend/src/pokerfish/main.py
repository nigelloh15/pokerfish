from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.pokerfish.core.manager import ConnectionManager
from src.pokerfish.routes.websocket import router as websocket_router
from src.pokerfish.db.redis import connect_to_redis, close_redis_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup logic
    redis = await connect_to_redis() 
    app.state.manager = ConnectionManager(redis)
    yield  # 🔁 App runs here

    # ✅ Shutdown logic
    await close_redis_connection()
    print("🔌 Redis closed")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}

app.include_router(websocket_router)
    
