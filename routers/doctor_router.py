from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from validation import micro_servicios
from models.doctor_model import Doctor_Model
from schemas.doctor import Doctor
from services.Doctor_Services import Doctor_Services
from database.database import Session
from fastapi.encoders import jsonable_encoder
from schemas.user import User
from auth.user_services import UserServices
from fastapi.security import OAuth2PasswordRequestForm


doctor_router = APIRouter()


@doctor_router.get("/doctor/get", tags=["doctor"])
async def search_id_doctor(id: int, current_user:  OAuth2PasswordRequestForm = Depends(UserServices.get_current_user_role(["doctor","admin"]))):
    if not current_user:
        raise HTTPException(status_code=401, detail="Access denied. Authentication credentials provided are invalid or missing.")
    with Session() as db:
        result = micro_servicios.search_id(Doctor_Model, db, id)
        if not result:
            raise HTTPException(status_code=404, detail="No doctor found with the provided ID.")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@doctor_router.get("/doctor/search/phone_number", tags=["doctor"])
def search_phone_number_doctor(phone_number: str, current_user: User = Depends(UserServices.get_current_user_role("doctor"))):
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Access denied. Authentication credentials provided are invalid or missing.")
    with Session() as db:
        result = Doctor_Services(db).search_phone_number_doctor(phone_number)
        if not result:
            raise HTTPException(status_code=404, detail="No doctor found with the provided phone number.")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
    

@doctor_router.put("/doctor/put", tags=["doctor"], dependencies=[Depends(UserServices.get_current_user_role("doctor"))])
def edit_doctor(id_doctor: int, doctor: Doctor):
    with Session() as db:
        try:
            return Doctor_Services(db).edit_doctor(id_doctor, doctor)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@doctor_router.delete("/doctor/remove/{id_doctor}/", tags=["doctor"], dependencies=[Depends(UserServices.get_current_user_role("doctor"))])
def remove_doctor(id_doctor: int):
    with Session() as db:
        return Doctor_Services(db).remove_doctor(id_doctor)
