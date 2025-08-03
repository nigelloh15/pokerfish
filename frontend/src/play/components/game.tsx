import Player from "./player";
import Card from "./card";
import type { GameState, PlayerState } from "../join";

interface GameProps {
  ws: WebSocket;  
  gamestate: GameState;
  name: string;
}

export default function Game({ ws, gamestate, name }: GameProps) {

  const fold = () => {
    console.log("Fold action triggered");
  }
  const call = () => {
    console.log("Call action triggered");
  }
  const raise = () => {
    console.log("Raise action triggered");
  }
  
  const player = gamestate.players.find(player => player.name === name);

  return (
    <div className="flex flex-col min-w-screen min-h-screen justify-center">
      <div className="flex flex-col gap-[2vh]">
        <div className="players text-center flex flex-row justify-evenly items-center">
          {gamestate.players.map((player: PlayerState, index: number) => (
            <Player key={index} name={player.name} money={1000} action="Call"/>
          ))}
        </div>
        <div className="communitycards flex flex-row justify-center items-center gap-[2vw]">
          <Card card={"9"} suit="♥" />
          <Card card={"9"} suit="♠"/>
          <Card card={"9"} suit="♦"/>
          <Card card={"9"} suit="♣"/>
          <Card card={"9"} suit="♣"/>
        </div>
        <div className="cards flex flex-row justify-center items-center gap-[2vw]">
          {player?.hand.map((card, index) => (
            <Card key={index} card={card[0]} suit={card[1]}/>
          ))}
        </div>
        <div className="money flex justify-center items-center">
          <div>
            $1000
          </div>
        </div>
        <div className="buttons flex flex-row gap-[2vw] justify-center items-center">
          <button className="action-button" onClick={fold}>Fold</button>
          <button className="action-button" onClick={call}>Call</button>
          <button className="action-button" onClick={raise}>Raise</button>
        </div>
      </div>
    </div>
  );

}
