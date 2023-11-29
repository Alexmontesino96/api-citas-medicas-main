from schemas.pacient import Pacient
from models.pacient import Pacient_Model
from common_services.micro_services import validate_existence_user_with_role
from fastapi.exceptions import HTTPException
from auth.user_services import UserServices
from sqlalchemy.exc import SQLAlchemyError



class Patient_Services:
    def __init__(self, db) -> None:
        self.db = db


    async def add_patient_db(self, patient_data: dict, username: str):
            """
            Adds a new patient to the database.

            Args:
                patient_data (dict): The data of the patient to be added.
                username (str): The username of the user performing the action.

            Returns:
                int: The ID of the newly added patient.

            Raises:
                HTTPException: If there is an error adding the patient to the database.
            """
            try:
                validate_existence_user_with_role("patient", username, self.db)
                new_patient = Pacient_Model(**patient_data)
                self.db.add(new_patient)
                self.db.flush()
                return new_patient.id

            except SQLAlchemyError as e:
                self.db.rollback
                raise HTTPException(status_code=500, detail=str(e))
        

        
    """Adaptar los siguientes metodos a la nueva estructura de la base de datos y los modelos"""
    def edit_patient(self, id: int, patient: Pacient):
        with self.db as db:
            result_db = self.search_patient_id(id)
            if result_db:
                result_db.update_with(patient)
                self.db.commit()
                return True
            else:
                return False
