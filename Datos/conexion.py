import os
import mysql.connector
from mysql.connector import Error

class ConexionBD:
    """Clase encargada exclusivamente de conectar Python con el servidor MySQL."""
    
    @staticmethod
    def obtener_conexion():
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "ecotech_db")
            )
            return conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None