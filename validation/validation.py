from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def validation_date(date: str):
    valid_date = datetime
    if date:
        try:
            # Trata de convertir la cadena en un objeto datetime
            if date != "string":
                valid_date = datetime.strptime(date, "%m/%d/%Y")
            # Si tiene éxito, retorna el objeto datetime
            return valid_date
        except ValueError:
            # Si falla, lanza un error con un mensaje personalizado
            raise ValueError("Date must be in MM/DD/YYYY format")


def validar_next_day(date_appointment: datetime) -> bool:
    fecha_actual = datetime.now().date()
    date_appointment_date = date_appointment.date()
    fecha_limite = fecha_actual + timedelta(days=1)  # Añadir un día a la fecha actual

    return date_appointment_date > fecha_limite  # Retorna True si la fecha ingresada es válida, de lo contrario, retorna False


def update_date(result_db, data_user):
    try:
        appointment_dict = data_user.model_dump()
        for attribute, value in appointment_dict.items():
            if getattr(result_db, attribute) != value and value != "string":
                setattr(result_db, attribute, value)

        return result_db
    except ValidationError as e:
        return JSONResponse(content={"message": f"Validation error: {e}"}, status_code=404)
