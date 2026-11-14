import os
import mysql.connector
from mysql.connector import Error

def inicializar_bd():
    """Crea la base de datos 'ecotech_db' y sus tablas en MySQL si no existen."""
    try:
        # Nos conectamos a MySQL usando variables de entorno o valores por defecto
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")
        )
        cursor = conexion.cursor()

        # 1. Crear la base de datos y seleccionarla
        cursor.execute("CREATE DATABASE IF NOT EXISTS ecotech_db")
        cursor.execute("USE ecotech_db")

        # 2. Tabla Departamento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departamento (
                idDepartamento INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL
            )
        ''')

        # 3. Tabla Empleado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Empleado (
                idEmpleado VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(150),
                telefono VARCHAR(30),
                correoElectronico VARCHAR(100),
                fechaInicioContrato DATE,
                salario DECIMAL(12, 2),
                idDepartamento INT,
                FOREIGN KEY (idDepartamento) REFERENCES Departamento(idDepartamento)
            )
        ''')

        # 4. Tabla Proyecto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Proyecto (
                idProyecto INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                fechaInicio DATE
            )
        ''')

        # 5. Tabla RegistroTiempo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS RegistroTiempo (
                idRegistro INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE,
                horasTrabajadas DECIMAL(5, 2),
                descripcionTareas TEXT,
                idEmpleado VARCHAR(20),
                idProyecto INT,
                FOREIGN KEY (idEmpleado) REFERENCES Empleado(idEmpleado),
                FOREIGN KEY (idProyecto) REFERENCES Proyecto(idProyecto)
            )
        ''')

        # 6. Tabla Usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuario (
                username VARCHAR(50) PRIMARY KEY,
                passwordCifrada VARCHAR(255) NOT NULL,
                rol VARCHAR(50) NOT NULL
            )
        ''')

        conexion.commit()
        print("¡Éxito! Base de datos 'ecotech_db' y tablas creadas en MySQL.")
    except Error as e:
        print(f"Error al crear la base de datos en MySQL: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    inicializar_bd()