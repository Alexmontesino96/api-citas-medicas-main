import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from validation import micro_servicios
from schemas.appointment import Appointment
from models.apointment_model import Appointment_Model
from fastapi.responses import JSONResponse
from models.doctor_model import Doctor_Model
from models.pacient import Pacient_Model
from fastapi.encoders import jsonable_encoder



class Appointment_Services:
    def __init__(self, db) -> None:
        self.db = db

    def show_appointment_id(self, id: int):

        result = micro_servicios.search_id(Appointment_Model, self.db, id)
        if not result:
            return JSONResponse(content={"message": "Appointment not found"}, status_code=400)
        return JSONResponse(content=jsonable_encoder(Appointment_Model.show_appointment(result)), status_code=200)

    def add_appointment(self, appointment: Appointment):

        try:
            result = micro_servicios.search_id(Doctor_Model, self.db, appointment.doctor_id)
            if not result:
                HTTPException(status_code=404, detail="Doctor in appointment not found")
            result = micro_servicios.search_id(Pacient_Model, self.db, appointment.patient_id)
            if not result:
                HTTPException(status_code=404, detail="Patient in appointment not found")

            new_appointment = Appointment_Model(**appointment.model_dump())

            self.db.add(new_appointment)
            self.db.commit()
            self.db.refresh(new_appointment)

            return JSONResponse(content={"message": "Appointment added successfully"}, status_code=200)
            
        except SQLAlchemyError as e:
            print(str(e))
            return e.detail

    def update_appointment(self, id: int, appointment: Appointment):

        try:

            result_db = micro_servicios.search_id(Appointment_Model, self.db, id)
            if result_db is None:
                return JSONResponse(content={"message": "Appointment not found"}, status_code=404)
            result_id_patient = micro_servicios.search_id_exist(Pacient_Model, self.db, appointment.patient_id)
            if not result_id_patient:
                return JSONResponse(content={"message": "Patient not found"}, status_code=404)
            result_id_doctor = micro_servicios.search_id_exist(Doctor_Model, self.db, appointment.doctor_id)
            if not result_id_doctor:
                return JSONResponse(content={"message": "Doctor not found"}, status_code=404)
            for key, value in appointment.model_dump().items():
                if getattr(result_db, key) != value:
                    setattr(result_db, key, value)
            self.db.commit()
            return JSONResponse(content={"message": "Update Successfully"}, status_code=200)
        except SQLAlchemyError as e:
            print(str(e))
            return e.detail

    def remove_appointment(self, id: int):
        result = micro_servicios.search_id(Appointment_Model, self.db, id)
        if not result:
            return JSONResponse(content={"message": "Appointment not found"}, status_code=400)
        self.db.delete(result)
        self.db.commit()
        return JSONResponse(content={"message": "Delete Successfully"})
