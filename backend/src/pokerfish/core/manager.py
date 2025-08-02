from typing import Dict, List, Optional
from fastapi import WebSocket
from pydantic import BaseModel
import json, random, string

from src.pokerfish.db.redis import redis_client

class PlayerState(BaseModel):
    name: str
    chips: int
    bet: int
    folded: bool
    is_turn: bool
    hand: Optional[List[str]] = None

class GameState(BaseModel):
    players: List[PlayerState] = []
    leader: Optional[str] = None
    community_cards: List[str] = []
    pot: int = 0
    round: str = "pre-flop"
    dealer_index: int = 0
    current_turn_index: int = 0
    min_bet: int = 0
    game_started: bool = False

class ConnectionManager:
    def __init__(self):
        self.websockets: Dict[WebSocket, Dict[str, str]] = {}
        self.rooms: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str, name: str):
        await websocket.accept()

        state = await self.load_state_from_redis(room)
        if state is None:
            await websocket.close(code=1008, reason="Room does not exist")
            return

        if name in [player.name for player in state.players]:
            await websocket.close(code=1008, reason="Name already taken in this room")
            return

        self.websockets[websocket] = {"room_code": room, "name": name}
        if room not in self.rooms:
            self.rooms[room] = []
        self.rooms[room].append(websocket)

        state.players.append(PlayerState(name=name, chips=1000, bet=0, folded=False, is_turn=False))
        if state.leader is None:
            state.leader = name

        await self.save_state_to_redis(room, state)
        await self.broadcast_room_update(room)

    async def disconnect(self, websocket: WebSocket, room: str, name: str):
        try:
            del self.websockets[websocket]
            self.rooms[room].remove(websocket)

            state = await self.load_state_from_redis(room)
            if state is None:
                print("Cannot get state")
                return

            state.players = [player for player in state.players if player.name != name]
            await self.save_state_to_redis(room, state)
        except ValueError:
            pass
        await self.broadcast_room_update(room)

    def create_room(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if redis_client is None:
                print("Not connected to redis")
                return
            if redis_client.get(f"game_state:{code}") is None:
                state = GameState()
                redis_client.set(f"game_state:{code}", state.json())
                self.rooms[code] = []
                return {"room_code": code}

    def delete_room(self, room: str):
        if redis_client is None:
            print("Not connected to redis")
            return
        redis_client.delete(f"game_state:{room}")
        if room in self.rooms:
            del self.rooms[room]

    async def broadcast(self, message: str, room: str):
        payload = json.loads(message)
        if room in self.rooms:
            for websocket in self.rooms[room]:
                await websocket.send_text(json.dumps(payload))

    async def broadcast_room_update(self, room: str):
        names = [self.websockets[ws]["name"] for ws in self.rooms[room]]
        state = await self.load_state_from_redis(room)
        if state is None:
            print("Cannot get state")
            return 
        leader = state.leader if state.leader else None
        message = json.dumps({"type": "room_update", "users": names, "leader": leader})
        for websocket in self.rooms[room]:
            await websocket.send_text(message)

    async def start_game(self, room: str):
        state = await self.load_state_from_redis(room)
        if state is None:
            print("Cannot get state")
            return
        state.game_started = True
        await self.save_state_to_redis(room, state)
        broadcast_message = json.dumps({"type": "start_game"})
        await self.broadcast(broadcast_message, room)

    async def get_state(self, room: str):
        state = await self.load_state_from_redis(room)
        return state.model_dump() if state else None

    async def save_state_to_redis(self, room: str, state: GameState):
        if redis_client is None:
            print("Not connected to redis")
            return
        redis_client.set(f"game_state:{room}", state.model_dump_json())

    async def load_state_from_redis(self, room: str) -> Optional[GameState]:
        if redis_client is None:
            print("Not connected to redis")
            return
        state_json = redis_client.get(f"game_state:{room}")
        if state_json:
            return GameState.model_validate(state_json)
        return None
