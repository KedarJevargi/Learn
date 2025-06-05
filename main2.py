from fastapi import FastAPI
import json


app=FastAPI()


def read_data():
    with open("patients.json","r") as f:
        data=json.load(f)
    return data    
        
@app.get("/")
def home():
    return{"message":"Patient Management System"}

@app.get("/about")
def about():
    return{"message":"A fully functional API to manage patients record"}


@app.get("/view")
def v():
    dat=read_data()
    return dat



