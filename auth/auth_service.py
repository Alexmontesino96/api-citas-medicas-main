import jwt
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from database.database import Session
from models.users_doctor import UserDoctor
from models.user_patient import UserPatient
from schemas.user import User
from schemas.doctor import Doctor
from schemas.pacient import Pacient
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthService:
    """
    This class provides methods to authenticate and register users, as well as to verify tokens.
    """

    @staticmethod
    async def search_username(username: str):
        with Session() as db:
            result = db.query(UserDoctor).filter(UserDoctor.username == username).first()
            if not result:
                return False
            return result

    @staticmethod
    def verify_token(token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception

            return username
            
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = await AuthService.search_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username",
            )
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )
        access_token = AuthService.create_access_token(data={"sub": user.username})
        return access_token

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def register_user_doctor(username: str, password: str, id_date_doctor: int):
        try:
            with Session() as db:
                hashed_password = pwd_context.hash(password)
                user_doctor = UserDoctor(username=username, hashed_password=hashed_password, id_doctor=id_date_doctor)
                db.add(user_doctor)
                db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def register_user_patient(username: str, password: str, id_date_patient: int):
        try:
            with Session() as db:
                hashed_password = pwd_context.hash(password)
                user_patient = UserPatient(username=username, hashed_password=hashed_password, id_doctor=id_date_doctor)
                db.add(user_patient)
                db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    

    @staticmethod
    def send_verification_code(email: str, code: str):
        # Configura las credenciales de tu cuenta de correo electrónico
        email_address = "alexmontesinocastro9@gmail.com"
        email_password = "Consuelo67*"

        # Crea el mensaje de correo electrónico
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = email
        msg['Subject'] = "Código de verificación"
        body = f"Tu código de verificación es: {code}"
        msg.attach(MIMEText(body, 'plain'))

        # Inicia sesión en el servidor de correo electrónico y envía el correo electrónico
        context = ssl.create_default_context()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=context)
            server.login(email_address, email_password)
            text = msg.as_string()
            server.sendmail(email_address, email, text)
        text = msg.as_string()
        server.sendmail(email_address, email, text)
        server.quit()

    @staticmethod 
    async def validate_user_type(user):
        if isinstance(user, Doctor) or isinstance(user, Patient):
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user type: User must be either a 'Doctor' or a 'Patient'."
            )
    @staticmethod
    async def validate_existing_user(username: str):
        user_exists = await AuthService.search_username(username)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating user, username already exists.",
            )
        return True
