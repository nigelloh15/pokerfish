from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Tuple
import random, string, json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, List[Tuple[WebSocket, str]]] = {}
        self.leaders: Dict[str, str] = {}  # room_code -> leader_name

    async def connect(self, websocket: WebSocket, room: str, name: str):
        await websocket.accept()

        if room not in self.rooms:
            await websocket.close(code=1008, reason="Room does not exist")
            return
        if name in [name for _, name in self.rooms[room]]:
            await websocket.close(code=1008, reason="Name already taken in this room")
            return

        if self.rooms[room] == []:
            self.leaders[room] = name

        self.rooms[room].append((websocket, name))
        await self.broadcast_room_update(room)

    async def disconnect(self, websocket: WebSocket, room: str, name: str):
        try:
            self.rooms[room].remove((websocket, name))
        except ValueError:
            pass
        await self.broadcast_room_update(room)

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
                await websocket.send_text(json.dumps({"message": message}))

    async def broadcast_room_update(self, room: str):
        names = [name for _, name in self.rooms[room]]
        leader = self.leaders.get(room)
        message = json.dumps({"type": "room_update", "users": names, "leader": leader})
        for websocket, _ in self.rooms[room]:
            await websocket.send_text(message)
                

manager = ConnectionManager()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/create-room")
def create_room():
    room = manager.create_room()
    return room


@app.websocket("/ws/{room}/{name}")
async def websocket_endpoint(websocket: WebSocket, room: str, name: str):

    await manager.connect(websocket, room, name)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{name}: {data}", room)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room, name)
        
    

