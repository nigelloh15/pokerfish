type CardProps = {
  card: string;
  suit: string;
};

export default function Card({card, suit}: CardProps) {
  
  let color: string;

  if (suit === "♦" || suit === "♥") {
    color = "text-red-500";
  }
  else {
    color = "text-black";
  }

  return (
    <div className={`relative h-[13vw] w-[10vw] border-[0.2vw] border-black border-solid rounded-[1vw] flex justify-center items-center ${color}`}>
      <div className="absolute top-[0.5vw] left-[1vw] text-[2vw]">
        {card}
      </div>
      <div className={`font-playfair text-[2vw]`}>
        {suit}
      </div>
    </div>
  );
}
