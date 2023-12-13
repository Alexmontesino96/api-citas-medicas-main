from database.database import Session
from fastapi import HTTPException
from models.doctor_model import Doctor_Model
from models.pacient import Pacient_Model
from models.apointment_model import Appointment_Model
from sqlalchemy.sql.expression import exists
from models.user_patient import UserPatient

def search_id_exist(class_type: Pacient_Model or Doctor_Model , db: Session, id: int):
    result_search = db.query(exists().where(class_type.id == id)).scalar()
    if result_search == None:
        return HTTPException(status_code=404, detail="No doctor found with the provided ID.", headers={"WWW-Authenticate": "Bearer"})
    else:
        return result_search

def search_id(class_type: Pacient_Model or Doctor_Model or Appointment_Model , db: Session, id: int):
    result_search = db.query(class_type).filter(class_type.id == id).first()
    print(result_search)
    if not result_search:
        return None
    else:
        return result_search
    
def search_patient_by_username(class_type: UserPatient, db: Session, username: str):
    result_user = db.query(class_type).filter(class_type.username == username).first()
    if not result_user:
        return None
    else:
        return result_user.pacient
