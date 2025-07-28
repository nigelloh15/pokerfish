from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.pokerfish.core.manager import ConnectionManager
from src.pokerfish.logic.input import handle_input
import json

router = APIRouter()
manager = ConnectionManager()

@router.get("/create-room")
def create_room():
    return manager.create_room()

@router.websocket("/ws/{room}/{name}")
async def websocket_endpoint(websocket: WebSocket, room: str, name: str):
    await manager.connect(websocket, room, name)
    try:
        while True:
            data = await websocket.receive_text()

            message = json.loads(data)
            await handle_input(message, manager, room, name)

    except WebSocketDisconnect:
        await manager.disconnect(websocket, room, name)
