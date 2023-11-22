from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from validation.micro_servicios import search_id
from schemas.doctor import Doctor
from schemas.pacient import Pacient
from services.Doctor_Services import Doctor_Services
from services.patient_services import Patient_Services
from database.database import Session
from auth.user_services import UserServices

login_router = APIRouter()

@login_router.post("/login", tags=["login"])
async def login(role: str, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user with the provided credentials and returns an access token if successful.

    Args:
        form_data (OAuth2PasswordRequestForm): The user's login credentials.
        auth_service (AuthService): An instance of the AuthService class.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    token = await UserServices.authenticate_user(form_data.username, form_data.password, role)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}
    
"""
This module contains the login routes for the medical appointments API.

It includes the following routes:
- POST /login: Authenticates a user and returns a JWT token.
- POST /register/patient: Registers a new patient user.
- POST /register/doctor: Registers a new doctor user.
"""


@login_router.post("/register/doctor", tags=["login"])
async def register_doctor(user_doctor: Doctor):
    user_data = user_doctor.get_user_data()
    doctor_data = user_doctor.get_doctor_data()
    with Session() as db:
        doctor_services = Doctor_Services(db)
        id_doctor = doctor_services.add_doctor(doctor_data)
        if not id_doctor:
            raise HTTPException(status_code=500, detail="Error creating doctor")

    if UserServices.register_user(user_data["username"], user_data["hashed_password"], "doctor", id_doctor):
        return {"message": "Doctor created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error creating doctor")
        

@login_router.post("/register/patient", tags=["login"])
async def register_patient(user_patient: Pacient):
    user_data = user_patient.get_user_data()
    patient_data = user_patient.get_patient_data()
    with Session() as db:
        patient_services = Patient_Services(db)
        id_patient = patient_services.add_patient(patient_data)
        if not id_patient:
            raise HTTPException(status_code=500, detail="Error creating patient")

    if UserServices.register_user(user_data["username"], user_data["hashed_password"], "patient", id_patient):
        return {"message": "Patient created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error creating patient")
