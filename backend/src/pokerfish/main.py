from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Tuple
import random, string

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, List[Tuple[WebSocket, str]]] = {}

    async def connect(self, websocket: WebSocket, room: str, name: str):
        await websocket.accept()
        self.rooms[room].append((websocket, name))

    async def disconnect(self, websocket: WebSocket, room: str, name: str):
        await websocket.close()
        self.rooms[room].remove((websocket, name))

    def create_room(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if code not in self.rooms:
                self.rooms[code] = []
                return {"room_code": code}

    def delete_room(self, room: str):
        if room in self.rooms:
            del self.rooms[room]

    async def broadcast(self, message: str, room: str):
        if room in self.rooms:
            for websocket, _ in self.rooms[room]:
                await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.websocket("/ws/{room}/{name}")
async def websocket_endpoint(websocket: WebSocket, room: str, name: str):
    if room not in manager.rooms:
        return {"error": "Room not found"}
    await manager.connect(websocket, room, name)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{name}: {data}", room)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room, name)
        
    

