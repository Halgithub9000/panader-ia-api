import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# load_dotenv()
# Configuración de la base de datos desde variables de entorno (para Cloud Run)
DB_HOST = os.getenv("DB_HOST", "localhost")  # La IP pública de tu Cloud SQL
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")  # ¡Cambia esto!
# Nombre de tu base de datos en Cloud SQL
DB_NAME = os.getenv("DB_NAME", "postgres")

# Construir la URL de conexión a PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos de SQLAlchemy ORM
Base = declarative_base()

# Función de utilidad para obtener una sesión de DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
