# Crear el mensaje del correo electrónico
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import os
from pydantic import EmailStr
from fastapi import HTTPException
from random import randint

    
    
def send_email_confirmation_code(addressee: EmailStr):
    """
    Sends an email with a confirmation code to the specified addressee.

    Parameters:
    - addressee (EmailStr): The email address of the recipient.

    Returns:
    - temporary_code (int): The generated confirmation code.

    Raises:
    - HTTPException: If there is an internal server error.
    """
    # Cargar las variables de entorno
    try:
        load_dotenv()
        remitente = os.getenv("USER_THERAPY")
        password = os.getenv("PASS")
        temporary_code = generate_confirmation_code()


        # Crea el mensaje
        msg = MIMEMultipart()
        msg['Subject'] = 'Confirmation code'
        msg['From'] = remitente
        msg['To'] = addressee

        with open('/Users/alexmontesino/Documents/GitHub/api-citas-medicas-main/email_services/code_confirmation_html.html', 'r') as html:
            html = html.read()
        # Reemplazar el marcador de posición con el código generado
        html = html.replace("123456", str(temporary_code))
        
        # Adjunta el mensaje al objeto MIMEMultipart
        msg.attach(MIMEText(html, 'html'))

        # Crea el servidor
        server = smtplib.SMTP('smtp.gmail.com: 587', timeout=6)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, addressee, msg.as_string())
        server.quit()


        return temporary_code
    
    except smtplib.SMTPConnectError:
        raise HTTPException(status_code=500, detail="No se pudo conectar al servidor de correo electrónico")
    except smtplib.SMTPServerDisconnected:
        raise HTTPException(status_code=500, detail="La conexión con el servidor de correo electrónico se perdió")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor -> {e}")


def generate_confirmation_code():
    """
    Genera un código de confirmación de 6 dígitos.

    Returns:
        int: Código de confirmación.
    """
    return randint(100000, 999999)