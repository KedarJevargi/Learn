from fastapi import FastAPI, Path, HTTPException, Query
import json


app=FastAPI()


def read_data():
    with open("patients.json","r") as f:
        data=json.load(f)
    return data    

def get_data_by_id(id):
        data=read_data()
        id=f"P0{id}"
        if id in data:
            return data[id]
        
        raise HTTPException(status_code=404,detail="Patient not found")
             
            

        
@app.get("/")
def home():
    return{"message":"Patient Management System"}

@app.get("/about")
def about():
    return{"message":"A fully functional API to manage patients record"}


@app.get("/views")
def v():
    dat=read_data()
    return dat



@app.get("/views/{p_id}")
def pid(p_id:str=Path(..., description="Can get patient info by id",example="1,2,3")):
    return get_data_by_id(p_id)




@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="Sort the data based on height,weight and BMI"),
                  order:str=Query('asc',description="Sort in asc or dsc order")):
     
     sort_data={"weight","height","bmi"}
     ord_data={"asc","dsc"}
     if sort_by not in sort_data:
          raise HTTPException(status_code=400,detail=f"Invalid entry select from {sort_data}")
     if order not  in ord_data:
          raise HTTPException(status_code=400,detail=f"Invalid entry select from {ord_data}")
     data=read_data()
     if order=="asc":
          re=False 
     else:
          re=True     

     sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=re)
     return sorted_data
     
