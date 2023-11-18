from schemas.doctor import Doctor
from models.doctor_model import Doctor_Model
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from validation import micro_servicios, validation


class Doctor_Services():
    """
    Clase que maneja los servicios relacionados con los doctores.
    """
    def __init__(self, db) -> None:
        self.db = db

    def add_doctor(self, doctor: dict):
        """
        Agrega un nuevo doctor a la base de datos.

        Args:
            doctor (Doctor): Objeto Doctor que se desea agregar.

        Returns:
            None
        """
        with self.db as db:
            try:
                new_doctor = Doctor_Model(**doctor)
                self.db.add(new_doctor)
                self.db.commit()
                print(new_doctor.id)
                return new_doctor.id
            except Exception as e:
                self.db.rollback()
                print(e)
                raise HTTPException(status_code=400, detail=str(e))
            finally:
                self.db.close()

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
        with self.db as db:
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
