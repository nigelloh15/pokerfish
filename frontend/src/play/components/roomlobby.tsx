type RoomLobbyProps = {
  roomCode: string;
  users: string[];
  isLeader: boolean;
  ws: WebSocket;
}

export default function RoomLobby({roomCode, users, isLeader, ws} : RoomLobbyProps) {

  const startGame = () => {
    ws.send(JSON.stringify({
      type: "start_game",
      room_code: roomCode
    }));
  }

  return (
      <div className="w-screen h-screen flex flex-col gap-[1vw] justify-center items-center">
        <div className="flex flex-col gap-[2vh]">
          <div className="flex flex-col gap-[0.5vh]">
            <div className="text-center">
              Room Code
            </div>
            <div className="input flex items-center">
              {roomCode}
            </div>
          </div>
          <div className="flex flex-col gap-[0.5vh]">
            <div className="text-center">
              Players
            </div>
            {users.map((user, index) => (
              <div key={index} className="input flex items-center">
                {user}
              </div>
            ))}
          </div>
          {isLeader &&
            <div className="flex justify-center items-center">
              <button onMouseUp={startGame}>
                Start
              </button>
            </div>
          }

        </div>
      </div>
  );
} 
