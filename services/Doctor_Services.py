from schemas.doctor import Doctor
from models.doctor_model import Doctor_Model
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from validation import micro_servicios, validation
from auth.user_services import UserServices
from sqlalchemy.exc import SQLAlchemyError
from common_services.micro_services import validate_existence_user_with_role


class Doctor_Services():
    
    def __init__(self, db) -> None:
        self.db = db

    async def add_doctor_db(self, doctor_data: dict, username: str):
            """
            Adds a new doctor to the database.

            Args:
                doctor_data (dict): A dictionary containing the doctor's data.
                username (str): The username of the user adding the doctor.

            Returns:
                int: The ID of the newly added doctor.

            Raises:
                HTTPException: If there is an error adding the doctor to the database.
            """
            try:
                validate_existence_user_with_role("doctor", username, self.db)

                new_doctor = Doctor_Model(**doctor_data)
                self.db.add(new_doctor)
                self.db.flush()
                return new_doctor.id

            except SQLAlchemyError as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=str(e))


    def edit_doctor(self, id_doctor: int, doctor: Doctor):
        """
        Edita un doctor existente en la base de datos.

        Args:
            id_doctor (int): ID del doctor que se desea editar.
            doctor (Doctor): Objeto Doctor con los nuevos datos.

        Returns:
            JSONResponse: Respuesta JSON con un mensaje de éxito o error.
        """
        with self.db as db:
            try:
                result = micro_servicios.search_id(Doctor_Model, self.db, id_doctor)
                if not result:
                    raise HTTPException(status_code=404, detail="No doctor found with the provided ID.")
                validation.update_date(result, doctor)
                self.db.commit()
                return JSONResponse(content={"message": "Update successfully"}, status_code=200)
            except Exception as e:
                self.db.rollback()
                print(e)
                raise HTTPException(status_code=500, detail="Internal server error")
            finally:
                self.db.close()

    def remove_doctor(self, id_doctor: int):
        """
        Elimina un doctor existente en la base de datos.

        Args:
            id_doctor (int): ID del doctor que se desea eliminar.

        Returns:
            JSONResponse: Respuesta JSON con un mensaje de éxito o error.
        """
        with self.db as db:
            try:
                result = micro_servicios.search_id(Doctor_Model, self.db, id_doctor)
                if not result:
                    return JSONResponse(content={"Deletion failed: No doctor found with the provided ID."}, status_code=404)
                self.db.delete(result)
                self.db.commit()
                return JSONResponse(content={"successfully": "Doctor deleted"}, status_code=200)
            except Exception as e:
                self.db.rollback()
                print(e)
                raise HTTPException(status_code=500, detail="Internal server error")
            finally:
                self.db.close()

    def search_phone_number_doctor(self, phone_number: str):
        """
        Busca un doctor por su número de teléfono.

        Args:
            phone_number (str): Número de teléfono del doctor que se desea buscar.

        Returns:
            Doctor: Objeto Doctor con los datos del doctor encontrado.
        """
        with self.db:
            try:
                result = self.db.query(Doctor_Model).filter(Doctor_Model.phone_number == phone_number).first()
                if not result:
                    raise HTTPException(status_code=404, detail="No doctor found with the provided phone number.")
                return result.users_doctor
            except Exception as e:
                print(e)
                raise HTTPException(status_code=500, detail="Internal server error")
            finally:
                self.db.close()
