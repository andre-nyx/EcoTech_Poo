from mysql.connector import Error, IntegrityError

from modelos.usuario import Usuario
from .conexion import ConexionBD


class UsuarioDAO:
    """Capa de Datos: guarda, consulta y elimina usuarios en MySQL."""

    @staticmethod
    def registrar_usuario(usuario: Usuario) -> bool:
        conexion = ConexionBD.obtener_conexion()
        if conexion is None:
            raise ConnectionError("No se pudo conectar con la base de datos.")
        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO Usuario (username, passwordCifrada, rol) VALUES (%s, %s, %s)"
            cursor.execute(sql, (usuario.username, usuario.password_cifrada, usuario.rol))
            conexion.commit()
            return True
        except IntegrityError as err:
            raise ValueError(f"El usuario '{usuario.username}' ya existe.") from err
        except Error as err:
            raise ConnectionError("No fue posible registrar el usuario. Intente nuevamente.") from err
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    @staticmethod
    def autenticar(username: str, password: str) -> Usuario:
        if not username or not password:
            raise ValueError("Debe ingresar usuario y contraseña.")
        
        Usuario.validar_username(username)
        if len(password) > 128:
            raise PermissionError("Usuario o contraseña incorrectos.")
        
        conexion = ConexionBD.obtener_conexion()
        if conexion is None:
            raise ConnectionError("No se pudo conectar con la base de datos.")
        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "SELECT username, passwordCifrada, rol FROM Usuario WHERE username = %s"
            cursor.execute(sql, (username,))
            fila = cursor.fetchone()
        except Error as err:
            raise ConnectionError("No fue posible validar las credenciales. Intente nuevamente.") from err
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

        if fila is None:
            raise PermissionError("Usuario o contraseña incorrectos.")
        usuario = Usuario.desde_hash(fila[0], fila[1], fila[2])
        if not usuario.iniciar_sesion(password):
            raise PermissionError("Usuario o contraseña incorrectos.")
        return usuario

    @staticmethod
    def eliminar_usuario(username: str) -> bool:
        """Elimina un usuario de MySQL de forma parametrizada."""
        if not username:
            raise ValueError("Debe indicar el nombre de usuario a eliminar.")

        conexion = ConexionBD.obtener_conexion()
        if conexion is None:
            raise ConnectionError("No se pudo conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Usuario WHERE username = %s"
            cursor.execute(sql, (username,))
            conexion.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"El usuario '{username}' no existe en la base de datos.")

            return True
        except Error as err:
            raise ConnectionError("No fue posible eliminar el usuario. Intente nuevamente.") from err
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    @staticmethod
    def actualizar_rol(username: str, nuevo_rol: str) -> bool:
        """Actualiza el rol de un usuario en MySQL de forma parametrizada."""
        if not username:
            raise ValueError("Debe indicar el nombre de usuario.")
        if nuevo_rol not in ("administrador", "empleado"):
            raise ValueError("Rol no válido. Solo se permite 'administrador' o 'empleado'.")

        conexion = ConexionBD.obtener_conexion()
        if conexion is None:
            raise ConnectionError("No se pudo conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Usuario SET rol = %s WHERE username = %s"
            cursor.execute(sql, (nuevo_rol, username))
            conexion.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"El usuario '{username}' no existe en la base de datos.")

            return True
        except Error as err:
            raise ConnectionError("No fue posible actualizar el rol. Intente nuevamente.") from err
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    @staticmethod
    def listar_usuarios() -> list:
        """Obtiene la lista de usuarios registrados con su respectivo rol."""
        conexion = ConexionBD.obtener_conexion()
        if conexion is None:
            raise ConnectionError("No se pudo conectar con la base de datos.")

        cursor = None
        try:
            cursor = conexion.cursor()
            # Solo consultamos username y rol para resguardar la seguridad
            cursor.execute("SELECT username, rol FROM Usuario ORDER BY username ASC")
            registros = cursor.fetchall()
            return registros
        except Error as err:
            raise ConnectionError("No fue posible obtener la lista de usuarios. Intente nuevamente.") from err
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
    
    @staticmethod
    def contar_usuarios() -> int:
        """Cantidad de usuarios registrados (sirve para saber si es el primero)."""
        conexion = ConexionBD.obtener_conexion()
        if conexion is None:
            raise ConnectionError("No se pudo conectar con la base de datos.")
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM Usuario")
            return cursor.fetchone()[0]
        except Error as err:
            raise ConnectionError("No fue posible consultar los usuarios. Intente nuevamente.") from err
        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()