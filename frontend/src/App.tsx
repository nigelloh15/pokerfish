import { useState } from "react";

type Response = {
  name: string;
  value: number;
}


function App() {

  const [name, setName] = useState<string>("");

  async function testBackend() {
    const response = await fetch('http://localhost:8000/test');
    const data = await response.json() as Response;
    setName(data.name);
  }

  return (
    <>
      <div>
        Here
      </div>
      <button className="bg-red-500 text-white" onClick={testBackend}>
        test
      </button>
      {name && (
        <div className="text-2xl">
          {name}
        </div>
      )}
    </>
  )
}

export default App
