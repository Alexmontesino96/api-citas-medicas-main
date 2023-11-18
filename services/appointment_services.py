import datetime

from validation import validation, micro_servicios
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

        result_doctor = micro_servicios.search_id(Doctor_Model, self.db, int(appointment.doctor_id))
        if not result_doctor:
            return JSONResponse(content={"message": "Doctor not found"}, status_code=404)

        else:
            result_patient = micro_servicios.search_id(Pacient_Model, self.db, int(appointment.patient_id))

        if result_patient:

            if validation.validar_next_day(datetime.datetime(appointment.date_appointment)):

                new_appointment = Appointment_Model(**appointment.model_dump())
                self.db.add(new_appointment)
                self.db.commit()
                return JSONResponse(content={"message": "Add Successfully"}, status_code=200)
            else:
                return JSONResponse(content={"message": "Date not valid"}, status_code=400)
        else:
            return JSONResponse(content={"message": "Patient` not found"}, status_code=404)

    def update_appointment(self, id: int, appointment: Appointment):

        result_db = micro_servicios.search_id(Appointment_Model, self.db, id)
        if not result_db:
            return JSONResponse(content={"message": "Patient not found"}, status_code=404)
        validation.update_date(result_db, appointment)
        self.db.commit()
        self.db.closed()

    def remove_appointment(self, id: int):
        result = micro_servicios.search_id(Appointment_Model, self.db, id)
        if not result:
            return JSONResponse(content={"message": "Appointment not found"}, status_code=400)
        self.db.delete(result)
        self.db.commit()
        return JSONResponse(content={"message": "Delete Successfully"})
