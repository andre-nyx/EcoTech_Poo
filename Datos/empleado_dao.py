from mysql.connector import Error, IntegrityError

# Permite que funcione tanto al darle Play directo como al importarlo desde main.py
try:
    from .conexion import ConexionBD
except ImportError:
    from conexion import ConexionBD


class EmpleadoDAO:
    """Clase encargada exclusivamente de las operaciones CRUD en MySQL (Principio SOLID)."""

    @staticmethod
    def registrar_departamento(nombre: str):
        """Registra un nuevo departamento en MySQL."""
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            # En MySQL se usa (%s) en lugar de (?) para consultas seguras parametrizadas
            sql = "INSERT INTO Departamento (nombre) VALUES (%s)"
            cursor.execute(sql, (nombre,))
            conexion.commit()
            print(f"Departamento '{nombre}' registrado exitosamente en MySQL.")
        except Error as e:
            print(f"Error al registrar departamento: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def registrar_empleado(id_empleado, nombre, direccion, telefono, correo, fecha_inicio, salario, id_departamento):
        """Registra un nuevo empleado en MySQL validando llaves duplicadas."""
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            sql = '''
                INSERT INTO Empleado 
                (idEmpleado, nombre, direccion, telefono, correoElectronico, fechaInicioContrato, salario, idDepartamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            '''
            datos = (id_empleado, nombre, direccion, telefono, correo, fecha_inicio, salario, id_departamento)
            cursor.execute(sql, datos)
            conexion.commit()
            print(f"Empleado '{nombre}' registrado exitosamente en MySQL.")
        except IntegrityError:
            print(f"Atención: El empleado con RUT {id_empleado} ya existe en el sistema.")
        except Error as e:
            print(f"Error de MySQL al registrar empleado: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def consultar_empleados():
        """Obtiene y retorna todos los empleados registrados en MySQL."""
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Empleado")
            empleados = cursor.fetchall()
            return empleados
        except Error as e:
            print(f"Error al consultar empleados: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_salario_empleado(id_empleado: str, nuevo_salario: float):
        """Actualiza el salario de un empleado mediante su RUT."""
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Empleado SET salario = %s WHERE idEmpleado = %s"
            cursor.execute(sql, (nuevo_salario, id_empleado))
            conexion.commit()
            print(f"Salario actualizado exitosamente para el RUT: {id_empleado}.")
        except Error as e:
            print(f"Error al actualizar salario: {e}")
        finally:
            cursor.close()
            conexion.close()

    @staticmethod
    def eliminar_empleado(id_empleado: str):
        """Elimina un empleado del sistema mediante su RUT."""
        conexion = ConexionBD.obtener_conexion()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Empleado WHERE idEmpleado = %s"
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            print(f"Empleado con RUT {id_empleado} eliminado del sistema.")
        except Error as e:
            print(f"Error al eliminar empleado: {e}")
        finally:
            cursor.close()
            conexion.close()


# ==========================================
# --- BLOQUE DE PRUEBA EN MYSQL ---
# ==========================================
if __name__ == "__main__":
    # 1. Registrar un departamento de prueba
    EmpleadoDAO.registrar_departamento("Desarrollo de Software")

    # 2. Registrar a Juan Pérez en MySQL
    EmpleadoDAO.registrar_empleado(
        "12345678-9", "Juan Pérez", "Av. Siempre Viva 123",
        "+56912345678", "juan.perez@ecotech.cl", "2026-10-11", 1500000.0, 1
    )

    # 3. Consultar empleados
    print("\n--- Lista de Empleados en MySQL ---")
    for emp in EmpleadoDAO.consultar_empleados():
        print(emp)

    # 4. Actualizar salario
    print("\n--- Actualizando Salario ---")
    EmpleadoDAO.actualizar_salario_empleado("12345678-9", 1850000.0)

    # 5. Volver a consultar
    print("\n--- Lista Actualizada en MySQL ---")
    for emp in EmpleadoDAO.consultar_empleados():
        print(emp)