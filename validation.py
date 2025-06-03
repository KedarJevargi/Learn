from pydantic import BaseModel, StrictInt, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name:Annotated[str,Field(max_length=20, 
                             title="Name of the patient", 
                             description="Give the name of the patient in less than 20 char", 
                             examples=['Kedar'])]
    email:Optional[EmailStr]=None
    age:StrictInt=Field(gt=18,le=120)
    weight:float=Field(gt=0)
    height:float
    married:bool=False
    allergies:Optional[List[str]]=None,Field(max_length=20)  # type: ignore
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains={"hdfc.com","icic.com","sbi.com"}
        domain_name=value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError("Not found")
        return value
    
    @field_validator('name')
    @classmethod

    def name_capital(cls,value):
        return value.upper()
    

    @model_validator(mode="after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("Age more than 60 — add emergency contact number.")
        return model

    @computed_field
    @property
    def bmi(self)->float:
        bmi=self.weight/(self.height)**2
        return bmi
        

#user_model
patient_info={"name":"kedar jevargi",
              "email":"Kedarjevargi@sbi.com",
              "age":19,
              "weight":55.5,
              "height":1.74,
              "married":True,
              "allergies":["dust","papaya"],
              "contact_details":{"phone":"1231231321"}
            }   

patient_1=Patient(**patient_info)

#upload data
def insert_patient_data(data:Patient):
    print(data.name)
    print(data.age)
    print(data.allergies)
    print(data.married)
    print(data.bmi)
    print("Created")

#update data
def update_patient_data(data:Patient):
    print(data.name)
    print(data.age)
    print("Updated")

insert_patient_data(patient_1)
print("\n")
update_patient_data(patient_1)



print(patient_1.model_dump_json())
# print(patient_1.model_dump())