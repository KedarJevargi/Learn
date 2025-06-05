from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, field_validator, computed_field
import json

app = FastAPI()

# ---------------------- Patient Model ---------------------- #
class Patient(BaseModel):
    name: str = Field(max_length=20)
    city: str = Field(max_length=20)
    age: int = Field(gt=1, le=121)
    gender: str
    height: float=Field(gt=0)
    weight: float=Field(gt=0)

    @field_validator("name")
    @classmethod
    def name_capital(cls, value):
        return value.capitalize()

    @field_validator("city")
    @classmethod
    def city_capital(cls, value):
        return value.capitalize()

    @field_validator("gender")
    @classmethod
    def check_gender(cls, value):
        value = value.capitalize()
        gen_data = {"Male", "Female"}
        if value in gen_data:
            return value
        raise HTTPException(status_code=400, detail=f"Invalid input. Expected one of: {gen_data}")

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        elif self.bmi < 35:
            return "Obesity Class I (Moderate)"
        elif self.bmi < 40:
            return "Obesity Class II (Severe)"
        else:
            return "Obesity Class III (Very Severe or Morbid)"


# ---------------------- File Handling ---------------------- #
def read_data():
    try:
        with open("patients.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def write_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

def get_data_by_id(id):
    data = read_data()
    pid = f"P0{id}"
    if pid in data:
        return data[pid]
    raise HTTPException(status_code=404, detail="Patient not found")


# ---------------------- Routes ---------------------- #
@app.get("/")
def home():
    return {"message": "Patient Management System"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage patients' records"}

@app.get("/views")
def view_all_patients():
    return read_data()

@app.get("/views/{p_id}")
def view_patient_by_id(p_id: str = Path(..., description="Patient ID", example="1")):
    return get_data_by_id(p_id)

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort the data based on 'height', 'weight', or 'bmi'"),
    order: str = Query('asc', description="Sort order: 'asc' or 'dsc'")
):
    valid_sort_fields = {"weight", "height", "bmi"}
    valid_orders = {"asc", "dsc"}

    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid entry. Select from {valid_sort_fields}")
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail=f"Invalid entry. Select from {valid_orders}")

    data = read_data()
    reverse = order == "dsc"

    # Ensure BMI is present for sorting
    for pid, record in data.items():
        h = record.get("height")
        w = record.get("weight")
        if h and w:
            record["bmi"] = round(w / (h ** 2), 2)

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse)
    return sorted_data

@app.post("/add")
def add_patient(patient: Patient):
    data = read_data()
    new_id = f"P0{len(data) + 1}"
    data[new_id] = patient.model_dump()
    write_data(data)
    return {"message": f"Patient added with ID {new_id}"}
