from fastapi import FastAPI

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

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/students/{id}")

async def fetch(id:int):
    if id in students:
        return{"Name":f"{students[id]}"}
    else:
        return "Not found"
    


@app.get("/add/{a}/{b}")
async def add(a:int,b:int):
    return{"Sum":a+b}


@app.get("/sub/{a}/{b}")
async def add(a:int,b:int):
    return{"Sub":a-b}

@app.get("/multiply/{a}/{b}")
async def add(a:int,b:int):
    return{"Sum":a*b}

