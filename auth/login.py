from fastapi import APIRouter, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm
from schemas.doctor import Doctor
from schemas.pacient import Pacient
from database.database import Session
from auth.user_services import UserServices
from auth.token_services import TokenServices
from auth.auth_services import AuthServices
from auth.token_services import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context
from common_services.micro_services import UserRole
from enum import Enum

login_router = APIRouter()
auth_service = AuthServices(TokenServices(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES), UserServices(pwd_context, Session()))


@login_router.post("/login", tags=["login"])
async def login(role: UserRole, form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.login_user(form_data.username, form_data.password, role)


@login_router.post("/validate_confirmation_code", tags=["login"])
async def validate_confirmation_code(username: str, confirmation_code: str, ):
    return await auth_service.validate_confirmation_code(username, confirmation_code)
    

@login_router.post("/register/doctor", tags=["login"])
async def register_doctor(user_doctor: Doctor):
    return await auth_service.register_doctor(user_doctor)


@login_router.post("/register/patient", tags=["login"])
async def register_patient(user_patient: Pacient):
    return await auth_service.register_patient(user_patient)
        

