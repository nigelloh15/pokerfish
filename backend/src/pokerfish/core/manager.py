from typing import Dict, List, Optional, Tuple
from fastapi import WebSocket
from pydantic import BaseModel
from redis.asyncio import Redis
import json, string, random
import asyncio

numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["♠", "♥", "♦", "♣"]

class PlayerState(BaseModel):
    name: str
    chips: int
    bet: int
    folded: bool
    is_turn: bool
    hand: Optional[Tuple[Tuple[str, str], Tuple[str, str]]] = None

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
    def __init__(self, redis: Redis):
        self.websockets: Dict[WebSocket, Dict[str, str]] = {}
        self.rooms: Dict[str, List[WebSocket]] = {}
        self.pubsub: Dict[str, asyncio.Task] = {}
        self.redis = redis

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

        if room not in self.pubsub:
            self.pubsub[room] = asyncio.create_task(self.listen_to_room(room))

        state.players.append(PlayerState(name=name, chips=1000, bet=0, folded=False, is_turn=False, hand=((numbers[0], suits[0]), (numbers[0], suits[1]))))
        if state.leader is None:
            state.leader = name

        await self.save_state_to_redis(room, state)
        await self.broadcast_room_update(room)

    async def disconnect(self, websocket: WebSocket):
        if websocket not in self.websockets:
            return
        info = self.websockets[websocket]
        room = info["room_code"]
        name = info["name"]

        del self.websockets[websocket]
        if room in self.rooms and websocket in self.rooms[room]:
            self.rooms[room].remove(websocket)

        state = await self.load_state_from_redis(room)
        if state is None:
            return

        state.players = [player for player in state.players if player.name != name]
        if state.leader == name:
            if len(state.players) > 0:
                state.leader = state.players[0].name
                print(state.leader)
        if not state.players:
            await self.delete_room(room)
            self.pubsub[room].cancel()
            del self.pubsub[room]
            return
        else:
            await self.save_state_to_redis(room, state)
            await self.broadcast_room_update(room)

    async def create_room(self) -> Dict[str, str]:
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            res = await self.redis.get(f"game_state:{code}")
            if res is None:
                state = GameState()
                await self.save_state_to_redis(code, state)
                self.rooms[code] = []
                return {"room_code": code}

    async def delete_room(self, room: str):
        await self.redis.delete(f"game_state:{room}")
        if room in self.rooms:
            del self.rooms[room]

    async def broadcast(self, message: dict, room: str):
        if room in self.rooms:
            text = json.dumps(message)
            for websocket in self.rooms[room]:
                await websocket.send_text(text)

    async def broadcast_room_update(self, room: str):
        if room not in self.rooms:
            return

        state = await self.load_state_from_redis(room)
        if state:
            await self.broadcast(state.model_dump(), room)
        else:
            print(f"Error: Game state for room {room} not found")

    async def listen_to_room(self, room:str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"game_state:{room}")

        print(f"Listening to room {room} for updates...")

        try:

            while True:
                msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                if msg and msg['type'] == 'message':
                    try:
                        data = json.loads(msg['data'])
                        await self.broadcast(data, room)
                    except Exception as e:
                        print(f"Error processing message in room {room}: {e}")

        except asyncio.CancelledError:

            print(f"Stopped listening to room {room}")
            await pubsub.unsubscribe(f"game_state:{room}")
            await pubsub.close()

    async def publish_to_room(self, room: str, state: GameState):
        await self.redis.publish(f"game_state:{room}", state.model_dump_json())

    async def start_game(self, room: str):
        state = await self.load_state_from_redis(room)
        if state is None:
            return
        state.game_started = True
        await self.save_state_to_redis(room, state)
        await self.broadcast(state.model_dump(), room)

    async def get_state(self, room: str) -> Optional[dict]:
        state = await self.load_state_from_redis(room)
        return state.model_dump() if state else None

    async def save_state_to_redis(self, room: str, state: GameState):
        await self.redis.set(f"game_state:{room}", state.model_dump_json(), ex=86400)

    async def load_state_from_redis(self, room: str) -> Optional[GameState]:
        state_json = await self.redis.get(f"game_state:{room}")
        if state_json:
            return GameState.model_validate_json(state_json)
        return None
