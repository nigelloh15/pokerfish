
function App() {

  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center">
      <div className="text-[10vw] font-playfair font-bold">
        PokerFish
      </div>
      <div className="flex flex-row gap-[2vw]">
        <button onMouseUp={() => {
          window.location.href = "/play";
      }} className="text-[2vw] rounded-[2vw] w-[10vw] cursor-pointer">
          PLAY
        </button>
        <button onMouseUp={() => {
          window.location.href = "/donate";
      }} className="text-[2vw] rounded-[2vw] w-[10vw] cursor-pointer">
          DONATE
        </button>
      </div>
    </div>
  )
}

export default App
