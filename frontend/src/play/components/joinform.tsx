type JoinFormProps = {
  nameRef: React.RefObject<HTMLInputElement | null>;
  roomCodeRef: React.RefObject<HTMLInputElement | null>;
  handleCreateRoom: () => void;
  handleJoinRoom: () => void;
  error: string;
};

export default function JoinForm({ nameRef, roomCodeRef, handleCreateRoom, handleJoinRoom, error}: JoinFormProps) {
  return (
    <div className="w-screen h-screen flex flex-col gap-[2vh] justify-center items-center">
      <div className="flex flex-col gap-[1.5vh]">
        <input ref={nameRef} className="input" type="text" placeholder={"Name"} />
        <input ref={roomCodeRef} className="input" type="text" placeholder={"Room Code"} />
        {error &&
          <div className="text-red-500 text-center absolute left-1/2 transform -translate-x-1/2 -translate-y-[120%]">{error}</div>
        }
      </div>
      <div className="flex flex-row gap-[1vw]">
        <button onMouseUp={handleCreateRoom}>
          Create Room
        </button>
        <button onMouseUp={handleJoinRoom}>
          Join Room
        </button>
      </div>
    </div>
  );
}
