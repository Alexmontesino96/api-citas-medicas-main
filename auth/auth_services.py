from fastapi import HTTPException
from auth.token_services import TokenServices
from auth.user_services import UserServices
from fastapi import status
from database.database import Session
from services.Doctor_Services import Doctor_Services
from services.patient_services import Patient_Services
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from schemas.doctor import Doctor
from schemas.pacient import Pacient
from common_services.micro_services import UserRole

class AuthServices:
    def __init__(self,token_services: TokenServices, user_services: UserServices):
        self.token_services = token_services
        self.user_services = user_services
        pass

    async def login_user(self, username: str, password: str, role: UserRole):
        token = self.user_services.authenticate_user(username, password, role)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"access_token": token, "token_type": "bearer"}
    

    async def register_doctor(self, user_doctor:Doctor):
            """
            Registers a doctor in the system.

            Args:
                user_doctor (Doctor): The doctor object containing user and doctor data.

            Returns:
                JSONResponse: The response indicating the success or failure of the registration process.
            """
            try:
                user_data = user_doctor.get_user_data()
                doctor_data = user_doctor.get_doctor_data()

                with Session() as db:
                    doctor_services = Doctor_Services(db)
                    id_doctor = await doctor_services.add_doctor_db(doctor_data, user_data["username"])                  

                    if not UserServices.register_user_db(user_data["username"], user_data["hashed_password"], "doctor", id_doctor, db):
                        db.rollback()
                        return JSONResponse(content={"message": "Failed to register user"}, status_code=500)

                    db.commit()
                    return JSONResponse(content={"message": "Doctor created successfully"}, status_code=200)
                
            except SQLAlchemyError as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=str(e))


    async def register_patient(self, user_patient: Pacient):
            """
            Register a new patient.

            Args:
                user_patient (Pacient): The patient object containing patient data.

            Returns:
                JSONResponse: The response containing the registration status.
            """
            try:
                patient_data = user_patient.get_patient_data()
                user_data = user_patient.get_user_data()

                with Session() as db:
                    patient_services = Patient_Services(db)
                    id_patient = await patient_services.add_patient_db(patient_data, user_data["username"])

                    if not UserServices.register_user_db(user_data["username"], user_data["hashed_password"], "patient", id_patient, db):
                        db.rollback()
                        return JSONResponse(content={"message": "Failed to register user"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    db.commit()
                    return JSONResponse(content={"message": "Patient created successfully"}, status_code=status.HTTP_200_OK)
            except SQLAlchemyError as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
