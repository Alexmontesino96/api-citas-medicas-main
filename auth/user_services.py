from fastapi import Depends, HTTPException
from database.database import Session
from common_services.micro_services import search_user_with_role
from passlib.context import CryptContext
from auth.token_services import TokenServices
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from models.users_doctor import UserDoctor
from models.user_patient import UserPatient
from auth.token_services import pwd_context





class UserServices:
    def __init__(self, pwd_context: CryptContext, db: Session):
        self.pwd_context = pwd_context
        self.db = db
    

    async def authenticate_user(username: str, password: str, role: str):
            """
            Authenticates a user with the provided username, password, and role.

            Args:
                username (str): The username of the user.
                password (str): The password of the user.
                role (str): The role of the user.

            Returns:
                str: The access token for the authenticated user.

            Raises:
                HTTPException: If the username is incorrect or the password is incorrect.
            """
            user = await search_user_with_role(role, username)

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username",
                )
            if TokenServices.match_password(password, user.hashed_password):
                access_token = TokenServices.create_access_token(username=username, role=role)
            return access_token
    


    def get_current_user_role(required_role: list) -> str:
            """
            Decorator function that checks if the current user has the required role.

            Args:
                required_role (list): A list of roles that the user must have.

            Returns:
                str: The token if the user has the required role.

            Raises:
                HTTPException: If the user does not have the required role.
            """

            def role_checker(token: str = Depends(TokenServices.verify_token)):
                user_role = token['role']
                if user_role not in required_role:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access forbidden: User does not have the required role '{required_role}'.",
                    )
                return token
            return role_checker
    

    async def validate_existing_user(username: str, user_type: str):
        if not search_user_with_role(user_type, username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username '{username}' already exists.",
            )
        return True
    


    def register_user(username: str, password: str, user_type: str, user_id: int):
        try:
            with Session() as db:
                
                user_exists = search_user_with_role(user_type, username)
                if user_exists:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

                hashed_password = pwd_context.hash(password)
                if user_type == "doctor":
                    user = UserDoctor(username=username, hashed_password=hashed_password, id_doctor=user_id)
                elif user_type == "patient":
                    user = UserPatient(username=username, hashed_password=hashed_password, pacient_id=user_id)
                else:
                    raise ValueError("Invalid user type")

                db.add(user)
                db.commit()
                return True
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        except ValueError as ve:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    