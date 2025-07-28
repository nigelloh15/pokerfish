from src.pokerfish.core.manager import ConnectionManager
from typing import Dict, Any

async def handle_input(input_data: Dict[str, Any], manager: ConnectionManager, room: str, name: str):
    print(input_data)

    if input_data["type"] == "start_game":
        await manager.start_game(room)

    elif input_data["type"] == "game_state":
        pass

    return
    
