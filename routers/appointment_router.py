from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.apointment_model import Appointment_Model
from validation import micro_servicios, validation
from schemas.appointment import Appointment
from services.appointment_services import Appointment_Services
from database.database import Session

appointment_router = APIRouter()


@appointment_router.get("/appointment/search/{id}", tags=["appointment"])
def search_appointment_id(id: int):
    db = Session()
    result = micro_servicios.search_id(Appointment_Model,db,id)
    if not result:
        return JSONResponse(content={"message":"Appointment not found"}, status_code= 400)
    db.close()
    return JSONResponse(content= jsonable_encoder(result), status_code=200)


@appointment_router.post("/appointment/add/", tags=["appointment"])
def add_appointment(appointment: Appointment):
    db = Session()

    return Appointment_Services(db).add_appointment(appointment)

@appointment_router.put("/appointment/update/", tags=["appointment"])
def update_appointment(id:int, appointment: Appointment):
    db = Session()

    return Appointment_Services(db).update_appointment(id, appointment)

@appointment_router.delete("/appointment/delete/{id}", tags=["appointment"])
def remove_appointment (id: int):
    db = Session()
    return Appointment_Services(db).remove_appointment(id)

