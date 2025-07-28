from typing import Dict, List, Tuple, Optional
from fastapi import WebSocket
from pydantic import BaseModel
import json, random, string

class PlayerState(BaseModel):
    name: str
    chips: int
    bet: int
    folded: bool
    is_turn: bool
    hand: Optional[List[str]] = None  # Only included for the player themselves

class GameState(BaseModel):
    type: str = "game_state"
    room_code: str
    players: List[PlayerState]
    community_cards: List[str] = []
    pot: int = 0
    round: str = "pre-flop"
    dealer_index: int = 0
    current_turn_index: int = 0
    min_bet: int = 0
    game_started: bool = False

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, List[Tuple[WebSocket, str]]] = {}
        self.state: Dict[str, str] = {}  


        """ 
        state json format

        {
          "type": "game_state",
          "room_code": "ABC123",
          "players": [
            {
              "name": "Player 1",
              "websocket": "<WebSocket>",
              "chips": 1500,
              "bet": 50,
              "folded": false,
              "is_turn": true,
              "hand": ["AS", "KH"]  // Only sent to the player themself
            },
            {
              "name": "Alice",
              "websocket": "<WebSocket>",
              "chips": 1200,
              "bet": 100,
              "folded": true,
              "is_turn": false
            }
          ],
          "community_cards": ["7H", "8C", "2D", "JC"], // Can reveal gradually
          "pot": 300,
          "round": "flop", 
          "dealer_index": 1,
          "current_turn_index": 0,
          "min_bet": 100,
          "game_started": true
        }

        """


    async def connect(self, websocket: WebSocket, room: str, name: str):
        await websocket.accept()

        if room not in self.rooms:
            await websocket.close(code=1008, reason="Room does not exist")
            return
        if name in [name for _, name in self.rooms[room]]:
            await websocket.close(code=1008, reason="Name already taken in this room")
            return

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
        message = json.loads(message)
        if room in self.rooms:
            for websocket, _ in self.rooms[room]:
                await websocket.send_text(json.dumps(message))

    async def broadcast_room_update(self, room: str):
        names = [name for _, name in self.rooms[room]]
        if self.rooms[room]:
            leader = self.rooms[room][0][1]
        else:
            leader = None
        message = json.dumps({"type": "room_update", "users": names, "leader": leader})
        for websocket, _ in self.rooms[room]:
            await websocket.send_text(message)

    async def start_game(self, room: str):
        broadcast_message = json.dumps({"type": "start_game"})
        await self.broadcast(broadcast_message, room)

    async def game_state(self, room: str, state: Dict):
        broadcast_message = json.dumps({"type": "game_state", "state": state})
        await self.broadcast(broadcast_message, room)






