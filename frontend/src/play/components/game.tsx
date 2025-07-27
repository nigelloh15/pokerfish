import Player from "./player";
import Card from "./card";

interface GameProps {
  ws: WebSocket;  
  players: Array<{name: string, money: number, action: string}>;
  communityCards: Array<{card: string, suit: string}>;
  playerCards: Array<{card: string, suit: string}>;
  currentPlayer: string;
  pot: number;
}

export default function Game({ ws, players, communityCards, playerCards, currentPlayer, pot }: GameProps) {

  const fold = () => {
    console.log("Fold action triggered");
  }
  const call = () => {
    console.log("Call action triggered");
  }
  const raise = () => {
    console.log("Raise action triggered");
  }

  return (
    <div className="flex flex-col w-screen h-screen justify-center">
      <div className="flex flex-col gap-[2vh]">
        <div className="players text-center flex flex-row justify-evenly items-center">
          <Player name={"Player 1"} money={1000} action="Call"/>
          <Player name={"Player 1"} money={1000} action="Call"/>
          <Player name={"Player 1"} money={1000} action="Call"/>
          <Player name={"Player 1"} money={1000} action="Call"/>
          <Player name={"Player 1"} money={1000} action="Call"/>
        </div>
        <div className="communitycards flex flex-row justify-center items-center gap-[2vw]">
          <Card card={"9"} suit="♥" />
          <Card card={"9"} suit="♠"/>
          <Card card={"9"} suit="♦"/>
          <Card card={"9"} suit="♣"/>
          <Card card={"9"} suit="♣"/>
        </div>
        <div className="cards flex flex-row justify-center items-center gap-[2vw]">
          <Card card={"9"} suit="♥" />
          <Card card={"9"} suit="♠"/>
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
