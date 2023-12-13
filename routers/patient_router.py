from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.pacient import Pacient_Model
from models.user_patient import UserPatient
from schemas.pacient import Pacient
from services.patient_services import Patient_Services
from database.database import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth.user_services import UserServices
from validation.micro_servicios import search_patient_by_username

patient_router = APIRouter()


@patient_router.get("/patient/", tags=["patient"])
def get_all_patient():
    db = Session()
    result = db.query(Pacient_Model).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@patient_router.get("/patient{id}", tags=["patient"])
def search_patient_id(id: int):
    db = Session()
    result, status_code = Patient_Services(db).search_patient_id(id)
    if status_code == 200:
        return JSONResponse(content=jsonable_encoder(result), status_code=status_code)
    else:
        return JSONResponse(content={"message": "Patient not found"}, status_code=status_code)
    
@patient_router.get("/patient/pending_appointment", tags=["patient"])
def get_patient_pending_appointment(current_user: OAuth2PasswordRequestForm = Depends(UserServices.get_current_user_role("patient"))):
    with Session() as db:
        result = search_patient_by_username(UserPatient, db, current_user["username"])
        if result:
            return JSONResponse(content=jsonable_encoder(result.appointments), status_code=200)
        else:
            return JSONResponse(content={"message": "Patient not found"}, status_code=404)


@patient_router.put("/patient/edit/", tags=["patient"])
def edit_patient(id: int, patient: Pacient):
    with Session() as db:
        if Patient_Services(db).edit_patient(id, patient):
            return JSONResponse(content={"message": "Edit Successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Patient not found"}, status_code=404)


@patient_router.delete("/patient/delete/{id}", tags=["patient"])
def delete_patient(id: int):
    db = Session()
    result = Patient_Services(db).search_patient_id(id)
    if result:
        db.delete(result)
        db.commit()
        return JSONResponse(content={"message": "Patient delete"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Patient not found"}, status_code=404)
