from fastapi import HTTPException
from models.user_patient import UserPatient
from models.users_doctor import UserDoctor
from database.database import Session

def search_user_with_role(rol, username):
    with Session() as db:
        if rol == 'paciente':
            tabla = UserPatient
        elif rol == 'doctor':
            tabla = UserDoctor
        else:
            raise ValueError({'error':'Rol inválido'})
        resultado = db.query(tabla).filter(tabla.username == username).first()
        if not resultado:
            return HTTPException(status_code=404, detail="No user found with the provided username.", headers={"WWW-Authenticate": "Bearer"})
        return resultado
