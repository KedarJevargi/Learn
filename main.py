from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

students = {
    101: "Alice",
    102: "Bob",
    103: "Charlie",
    104: "David",
    105: "Eva",
    106: "Frank",
    107: "Grace",
    108: "Hannah",
    109: "Ivan",
    110: "Julia"
}

class Values(BaseModel):
    a: int
    b: int

answers = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/students")
async def fetch(id: int):
    if id in students:
        return {"Name": students[id]}
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/add")
async def add(val: Values):
    ans = val.a + val.b
    answers.append(ans)
    return {"Message": "Addition successful", "Result": ans}

@app.post("/sub")
async def sub(val: Values):
    ans = val.a - val.b
    answers.append(ans)
    return {"Message": "Subtraction successful", "Result": ans}

@app.post("/multiply")
async def multiply(val: Values):
    ans = val.a * val.b
    answers.append(ans)
    return {"Message": "Multiplication successful", "Result": ans}

@app.get("/answers")
async def get_answers():
    return {"Answers": answers}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
