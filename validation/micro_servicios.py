from database.database import Session
from fastapi import HTTPException


def search_id(class_type, db: Session, id: int):
    result_search = db.query(class_type).filter(class_type.id == id).first()
    if not result_search:
        return HTTPException(status_code=404, detail="No doctor found with the provided ID.", headers={"WWW-Authenticate": "Bearer"})
    else:
        return result_search
