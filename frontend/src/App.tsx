
function App() {

  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center">
      <div className="text-[10vw] font-playfair">
        PokerFish
      </div>
      <a href="/play">
        <button className="text-[2vw] rounded-[2vw] w-[10vw] cursor-pointer">
          PLAY
        </button>
      </a>
    </div>
  )
}

export default App
