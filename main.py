# from fastapi import FastAPI

# app = FastAPI()

# students = {
#     101: "Alice",
#     102: "Bob",
#     103: "Charlie",
#     104: "David",
#     105: "Eva",
#     106: "Frank",
#     107: "Grace",
#     108: "Hannah",
#     109: "Ivan",
#     110: "Julia"
# }

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}



# @app.get("/students/{id}")

# async def fetch(id:int):
#     if id in students:
#         return{"Name":f"{students[id]}"}
#     else:
#         return "Not found"
    


# @app.get("/add/{a}/{b}")
# async def add(a:int,b:int):
#     return{"Sum":a+b}


# @app.get("/sub/{a}/{b}")
# async def add(a:int,b:int):
#     return{"Sub":a-b}

# @app.get("/multiply/{a}/{b}")
# async def add(a:int,b:int):
#     return{"Sum":a*b}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/add/{a}/{b}")
async def add(a: int, b: int):
    return {"Sum": a + b}

@app.get("/sub/{a}/{b}")
async def sub(a: int, b: int):
    return {"Sub": a - b}

@app.get("/multiply/{a}/{b}")
async def multiply(a: int, b: int):
    return {"Product": a * b}
