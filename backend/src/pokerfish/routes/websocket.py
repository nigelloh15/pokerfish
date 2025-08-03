from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from src.pokerfish.core.manager import ConnectionManager
from src.pokerfish.logic.input import handle_input
import json

router = APIRouter()

@router.get("/create-room")
async def create_room(request: Request):
    manager: ConnectionManager = request.app.state.manager
    return await manager.create_room()

@router.websocket("/ws/{room}/{name}")
async def websocket_endpoint(websocket: WebSocket, room: str, name: str):
    manager: ConnectionManager = websocket.app.state.manager
    await manager.connect(websocket, room, name)
    try:
        while True:
            data = await websocket.receive_text()

            message = json.loads(data)
            await handle_input(message, manager, room, name)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
