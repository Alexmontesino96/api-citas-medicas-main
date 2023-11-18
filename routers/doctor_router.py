from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from validation import micro_servicios, validation
from models.doctor_model import Doctor_Model
from schemas.doctor import Doctor
from services.Doctor_Services import Doctor_Services
from database.database import Session
from fastapi.encoders import jsonable_encoder
from auth.auth_service import AuthService
from schemas.user import User
from pydantic import EmailStr


doctor_router = APIRouter()
auth_handler = AuthService()

@doctor_router.get("/doctor/get", tags=["doctor"])
def search_id_doctor(id: int, current_user: User = Depends(auth_handler.verify_token)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Access denied. Authentication credentials provided are invalid or missing.")
    with Session() as db:
        result = micro_servicios.search_id(Doctor_Model, db, id)
        if not result:
            raise HTTPException(status_code=404, detail="No doctor found with the provided ID.")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@doctor_router.get("/doctor/search/phone_number", tags=["doctor"])
def search_phone_number_doctor(phone_number: str, current_user: User = Depends(auth_handler.verify_token)):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Access denied. Authentication credentials provided are invalid or missing.")
    with Session() as db:
        result = Doctor_Services(db).search_phone_number_doctor(phone_number)
        if not result:
            raise HTTPException(status_code=404, detail="No doctor found with the provided phone number.")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    

@doctor_router.put("/doctor/put", tags=["doctor"], dependencies=[Depends(auth_handler.verify_token)])
def edit_doctor(id_doctor: int, doctor: Doctor):
    with Session() as db:
        try:
            return Doctor_Services(db).edit_doctor(id_doctor, doctor)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@doctor_router.delete("/doctor/remove/{id_doctor}/", tags=["doctor"], dependencies=[Depends(auth_handler.verify_token)])
def remove_doctor(id_doctor: int):
    with Session() as db:
        return Doctor_Services(db).remove_doctor(id_doctor)
