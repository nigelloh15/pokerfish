type PlayerProps = {
  name: string;
  money: number;
  action: string;
};

export default function Player( {name, money, action}: PlayerProps) {

  return (
    <div className="flex flex-col justify-center items-center">
      <div>
        {name}
      </div>
      <div>
        ${money}
      </div>
      <div>
        {action}
      </div>
    </div>
  );
}
