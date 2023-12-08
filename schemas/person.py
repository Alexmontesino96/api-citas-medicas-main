from pydantic import BaseModel, Field, EmailStr, validator
from validation import validation
from typing import Optional
from common_services.micro_services import UserRole, Gender_User

class Person(BaseModel):
    """Model representing a person in the medical appointment system.

    Args:
        first_name (str): Person's first name.
        middle_name (str, optional): Person's middle name. Defaults to None.
        last_name (str): Person's last name.
        email (EmailStr): Person's email address.
        phone_number (str, optional): Person's phone number. Defaults to "7860000000".
        address (str): Person's address.
        birthdate (str, optional): Person's birthdate in "YYYY-MM-DD" format.
        gender (str, optional): Person's gender. Must be one of "M", "F", "X" or "O".
        role (List[str], optional): Person's role in the system. Must be one of "patient" or "doctor". Defaults to ["patient"].

    Raises:
        ValueError: If the role is not one of the valid options.
        ValueError: If the birthdate is not in the correct format.
        ValueError: If the gender is not one of the valid options.
        ValueError: If the phone number does not contain only digits or does not have a length of 10 characters.

    Returns:
        Person: An instance of the Person class.
    """
    first_name: str = Field(example = ["Name"], min_length=1, max_length=50, repr=True)
    middle_name: str = Field(None, max_length=50, min_length=1, validate_default=True)
    last_name: str = Field(examples=["Your Lastname"],min_length=1, max_length=50, repr=True)
    email: EmailStr = Field(examples= ["user@gmail.com"])
    phone_number: str = Field(examples= ["7861234567"],max_length=10, min_length=10)
    address: str = Field(examples=["123 Main St, Miami, FL 33131"])
    birthdate: str = Field(examples=["MM/DD/YYYY"])
    gender: Gender_User = Field(default= Gender_User.OTRO, examples=["M","F","X","O"])
    role: UserRole = Field(examples=["patient","doctor"])

    def is_doctor(self):
        return "doctor" in self.role.value

    def is_patient(self):
        return "patient" in self.role.value


    @validator("birthdate")
    def validate_birthdate(cls, value):
        valid_date = validation.validation_date(value,"%m/%d/%Y")
        return valid_date


    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not value.isdigit():
            raise ValueError("phone_number must only contain digits")
        if len(value) != 10:
            raise ValueError("phone_number must be 10 digits long")
        return value
