from fastapi import FastAPI
from routers.doctor_router import doctor_router
from routers.patient_router import patient_router
from database.database import Base, engine
from routers.appointment_router import appointment_router
from midleware.middleware import ErrorHandler
from auth.login import login_router
from routers.get_init import get_welcome_message


app = FastAPI()
app.title = "Medical Center"
app.version = "2.0"
app.add_middleware(ErrorHandler)
app.include_router(get_welcome_message)
app.include_router(login_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)
Base.metadata.create_all(bind=engine)
