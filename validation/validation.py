from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from pydantic import ValidationError


from datetime import datetime

def validation_date(date: str, date_format: str = "%m/%d/%Y"):
    """
    Validates a date string based on a given date format.

    Args:
        date (str): The date string to be validated.
        date_format (str, optional): The format of the date string. Defaults to "%m/%d/%Y".

    Returns:
        datetime.datetime: The validated date as a datetime object.

    Raises:
        ValueError: If the date string is empty.
        ValueError: If the date is in the future.
        ValueError: If the date string is not in the specified format.
    """
    if not date:
        raise ValueError("Date must not be empty")

    try:
        valid_date = datetime.strptime(date, date_format)
        # Additional check: ensure the date is not in the future
        if valid_date > datetime.now():
            raise ValueError("Date must not be in the future")
        return valid_date
    except ValueError:
        raise ValueError(f"Date must be in {date_format} format")



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
