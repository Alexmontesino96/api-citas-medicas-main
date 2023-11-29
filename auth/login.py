from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.doctor import Doctor
from schemas.pacient import Pacient
from database.database import Session
from auth.user_services import UserServices
from auth.token_services import TokenServices
from auth.auth_services import AuthServices
from auth.token_services import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context
from common_services.micro_services import UserRole


login_router = APIRouter()
auth_service = AuthServices(TokenServices(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES), UserServices(pwd_context, Session()))

@login_router.post("/login", tags=["login"])

async def login(role: UserRole, form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.login_user(form_data.username, form_data.password, role)
    


@login_router.post("/register/doctor", tags=["login"])

async def register_doctor(user_doctor: Doctor):
    return await auth_service.register_doctor(user_doctor)

@login_router.post("/register/patient", tags=["login"])

async def register_patient(user_patient: Pacient):
    return await auth_service.register_patient(user_patient)
        

