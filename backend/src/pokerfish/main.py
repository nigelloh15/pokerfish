from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestItem(BaseModel):
    name: str
    value: int

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/test", response_model=TestItem)
def test():
    return {"name": "Test Item", "value": 100}
