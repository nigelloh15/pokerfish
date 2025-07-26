import { useState, useRef } from "react";
import JoinForm from "./components/joinform";
import RoomLobby from "./components/roomlobby";

export default function Join() {

  const [connected, setConnected] = useState(false);
  const [roomCode, setRoomCode] = useState("");
  const [name, setName] = useState("");
  const [users, setUsers] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [leader, setLeader] = useState("");
  const nameRef = useRef<HTMLInputElement>(null);
  const roomCodeRef = useRef<HTMLInputElement>(null);

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

    const room = roomCodeRef.current.value;
    await connectToRoom(room);
  }

  const connectToRoom = async (room: string) => {
    // Logic to connect to a room

    if (nameRef.current && nameRef.current.value) {
      setName(nameRef.current?.value);
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
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "room_update") {
        setUsers(message.users);
        setLeader(message.leader);
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

  const isLeader = leader === name;

  if (connected) {
    return (
      <RoomLobby roomCode={roomCode} users={users} isLeader={isLeader}/>
    );
  }

  return (
    <JoinForm nameRef={nameRef} roomCodeRef={roomCodeRef} handleCreateRoom={handleCreateRoom} handleJoinRoom={handleJoinRoom} error={error} />
  );
}
