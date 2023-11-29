import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base


nombre_usuario = 'Alexmon96'
contraseña = 'Alexmon96'
host = 'localhost'
nombre_base_datos = 'medical_center'

# Crea la URL de la base de datos
database_url = f"mysql+mysqlconnector://{nombre_usuario}:{contraseña}@{host}/{nombre_base_datos}"

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

