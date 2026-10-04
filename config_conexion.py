"""Conexión a SQL Server
Establece la conexión utilizando SQLAlchemy y pyodbc leyendo
las variables de entorno desde el archivo .env."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Cargar automáticamente las variables de entorno desde el archivo .env local
load_dotenv()

def obtener_engine() -> Engine:
    """
    Construye y retorna un Engine de SQLAlchemy para SQL Server.
    Lee la configuración desde variables de entorno.
    Soporta Autenticación Integrada de Windows y Usuario/Contraseña.
    """
    servidor = os.getenv("DB_SERVER", "localhost")
    base_datos = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    trusted = os.getenv("DB_TRUSTED_CONNECTION", "yes").lower() in ("yes", "true", "1")

    if not base_datos:
        raise ValueError(
            "Error: Falta definir la variable de entorno 'DB_NAME' en tu archivo .env"
        )

    # Formatear el driver para la URL de conexión (reemplaza espacios por +)
    driver_format = driver.replace(" ", "+")

    usuario = os.getenv("TP2_USUARIO") or os.getenv("DB_USER")
    password = os.getenv("TP2_PASSWORD") or os.getenv("DB_PASSWORD")

    if trusted or not (usuario and password):
        # Autenticación Integrada de Windows (recomendada para entorno local)
        cadena = (
            f"mssql+pyodbc://@{servidor}/{base_datos}?"
            f"driver={driver_format}&trusted_connection=yes"
            f"&Encrypt=yes&TrustServerCertificate=yes"
        )
    else:
        # Autenticación por Usuario y Contraseña de SQL Server
        cadena = (
            f"mssql+pyodbc://{usuario}:{password}@{servidor}/{base_datos}?"
            f"driver={driver_format}"
            f"&Encrypt=yes&TrustServerCertificate=yes"
        )

    # fast_executemany=True agrupa inserciones por lotes para el ETL
    return create_engine(cadena, fast_executemany=True)

def probar_conexion() -> bool:
    """Prueba rápida que ejecuta una consulta SQL real para verificar el acceso."""
    try:
        engine = obtener_engine()
        with engine.connect() as conn:
            query = text("SELECT DB_NAME() AS bd, @@VERSION AS version;")
            res = conn.execute(query).fetchone()
            print("\n==========================================")
            print(" ¡CONEXIÓN EXITOSA A SQL SERVER!")
            print(f" Base de datos conectada: {res.bd}")
            print("==========================================\n")
            return True
    except Exception as e:
        print("\n==========================================")
        print(" ERROR AL CONECTAR CON LA BASE DE DATOS:")
        print(e)
        print("==========================================\n")
        return False

if __name__ == "__main__":
    probar_conexion()

