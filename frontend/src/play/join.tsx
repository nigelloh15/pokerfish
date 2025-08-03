import { useState, useRef } from "react";
import JoinForm from "./components/joinform";
import RoomLobby from "./components/roomlobby";
import Game from "./components/game";


export interface PlayerState {
  name: string;
  chips: number;
  bet: number;
  folded: boolean;
  is_turn: boolean;
  hand: string[]; 
}

export interface GameState {
  players: PlayerState[];
  leader: string;              
  community_cards: string[];
  pot: number;
  round: string;               // e.g., "pre-flop", "flop", etc.
  dealer_index: number;
  current_turn_index: number;
  min_bet: number;
  game_started: boolean;
}

export default function Join() {

  const [connected, setConnected] = useState(false);
  const [roomCode, setRoomCode] = useState("");
  const [error, setError] = useState("");
  const [name, setName] = useState("");
  const nameRef = useRef<HTMLInputElement>(null);
  const roomCodeRef = useRef<HTMLInputElement>(null);

  const [state, setState] = useState<GameState>();

  const websocket = useRef<WebSocket | null>(null);

  const handleCreateRoom = async () => {
    // Logic to create a room
    if (!nameRef.current || !nameRef.current.value) {
      setError("Name is required");
      return;
    }

    const res = await fetch("http://localhost:8000/create-room")
    const data = await res.json();
    await connectToRoom(data.room_code);
  };

  const handleJoinRoom = async () => {
    if (!roomCodeRef.current || !roomCodeRef.current.value) {
      setError("Room code is required");
      return;
    }
    if (!nameRef.current || !nameRef.current.value) {
      setError("Name is required");
      return;
    }

    const room = roomCodeRef.current.value.toUpperCase();
    await connectToRoom(room);
  }

  const connectToRoom = async (room: string) => {
    // Logic to connect to a room

    if (nameRef.current && nameRef.current.value) {
      setName(nameRef.current.value);
    }
    else {
      setError("Name is required");
      return;
    }

    const ws = new WebSocket(`ws://localhost:8000/ws/${room}/${nameRef.current.value}`);

    ws.onopen = () => {
      console.log("Connected to room:", room);
      setRoomCode(room);
      setConnected(true);
      websocket.current = ws; // Store the WebSocket instance
    };

    ws.onmessage = (event) => {
      const message: GameState = JSON.parse(event.data);

      const players = message.players.map(player => player.name);
      
      if (message != state) {
        setState(message);
      }

      console.log("Message from server:", message);
      // Handle incoming messages here
    }

    ws.onclose = (event) => {
      if (event.code == 1008) {
        console.error(event.reason);
      }
      console.log("Disconnected from room:", room);
      setConnected(false);
    }
  }

  const isLeader = state?.leader === name;
  const players = state?.players.map(player => player.name) || []
  const gameStarted = state?.game_started || false;

  if (gameStarted && state && websocket.current) {
    return (
      <Game ws={websocket.current} gamestate={state} name={name} />
    );
  }

  else if (connected && websocket.current) {
    return (
      <RoomLobby roomCode={roomCode} users={players} isLeader={isLeader} ws={websocket.current} />
    );
  }

  return (
    <JoinForm nameRef={nameRef} roomCodeRef={roomCodeRef} handleCreateRoom={handleCreateRoom} handleJoinRoom={handleJoinRoom} error={error} />
  );
}
