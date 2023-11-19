from validation import micro_servicios, validation
from schemas.pacient import Pacient
from models.pacient import Pacient_Model


class Patient_Services:
    def __init__(self, db) -> None:
        self.db = db

    def search_patient_id(self, id: int):
        with self.db as db:
            return micro_servicios.search_id(Pacient_Model, self.db, id)

    def add_patient(self, patient: dict):
        with self.db as db:
            try:
                new_patient = Pacient_Model(**patient)
                self.db.add(new_patient)
                self.db.commit()
                id_patient = new_patient.id
                return id_patient
            except Exception as e:
                self.db.rollback()
                self.db.flush()
                raise Exception(e)
            finally:
                self.db.close()

    def edit_patient(self, id: int, patient: Pacient):
        with self.db as db:
            result_db = self.search_patient_id(id)
            if result_db:
                result_db.update_with(patient)
                self.db.commit()
                return True
            else:
                return False
