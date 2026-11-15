import hashlib
import hmac
import os
import re

_ITERACIONES = 600_000
_PATRON_USERNAME = re.compile(r"[A-Za-z0-9_.-]{3,30}")
_ROLES_VALIDOS = ("administrador", "empleado")


def _hashear(password: str) -> str:
    """Convierte la contraseña en un texto irreconocible (hash con sal)."""
    sal = os.urandom(16)
    resultado = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sal, _ITERACIONES)
    return f"pbkdf2_sha256${_ITERACIONES}${sal.hex()}${resultado.hex()}"


class Usuario:
    def __init__(self, username: str, password: str, rol: str = "empleado"):
        self.username = username          # pasa por el setter, que valida
        self.rol = rol                    # pasa por el setter, que valida
        self.__password_cifrada = _hashear(self._validar_password(password))
        self.__sesion_activa = False

    @classmethod
    def desde_hash(cls, username: str, password_cifrada: str, rol: str):
        """Crea un Usuario a partir de lo que viene de la BD (la clave ya está hasheada)."""
        usuario = cls.__new__(cls)
        usuario.username = username
        usuario.rol = rol
        if not password_cifrada:
            raise ValueError("El hash de la contraseña no puede estar vacío.")
        usuario.__password_cifrada = password_cifrada
        usuario.__sesion_activa = False
        return usuario

    @staticmethod
    def _validar_password(password: str) -> str:
        if not isinstance(password, str) or not password.strip():
            raise ValueError("La contraseña no puede estar vacía.")
        if len(password) < 8 or len(password) > 128:
            raise ValueError("La contraseña debe tener entre 8 y 128 caracteres.")
        return password

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, valor: str):
        self.__username = self.validar_username(valor)

    @staticmethod
    def validar_username(valor: str) -> str:
        if not isinstance(valor, str) or not _PATRON_USERNAME.fullmatch(valor):
            raise ValueError("El usuario debe tener de 3 a 30 caracteres: "
                             "letras, números, punto, guion o guion bajo.")
        return valor

    @property
    def rol(self) -> str:
        return self.__rol

    @rol.setter
    def rol(self, valor: str):
        if valor not in _ROLES_VALIDOS:
            raise ValueError("Rol no válido.")
        self.__rol = valor

    @property
    def password_cifrada(self) -> str:
        return self.__password_cifrada

    def cambiar_password(self, nueva_password: str) -> None:
        self.__password_cifrada = _hashear(self._validar_password(nueva_password))

    def verificar_password(self, password: str) -> bool:
        if not isinstance(password, str) or not password:
            return False
        try:
            _, iteraciones, sal_hex, hash_hex = self.__password_cifrada.split("$")
            calculado = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                            bytes.fromhex(sal_hex), int(iteraciones))
        except ValueError:
            return False
        return hmac.compare_digest(calculado.hex(), hash_hex)

    def iniciar_sesion(self, password: str) -> bool:
        self.__sesion_activa = self.verificar_password(password)
        return self.__sesion_activa

    def acceder_modulo(self) -> None:
        if not self.__sesion_activa:
            raise PermissionError("Debe iniciar sesión para acceder a este módulo.")

    def exigir_rol(self, rol_requerido: str) -> None:
        self.acceder_modulo()
        if self.__rol != rol_requerido:
            raise PermissionError("No tiene permisos para realizar esta acción.")

    def _validar_entradas(self) -> bool:  # Método protegido (-) del UML
        return bool(self.__username and self.__password_cifrada)

    def obtenerInformacion(self) -> dict:
        return {"username": self.__username, "rol": self.__rol}