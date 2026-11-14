# modelos/empleado.py
from datetime import date


class Empleado:
    def __init__(self, id_empleado: str, nombre: str, direccion: str, 
                 telefono: str, correo_electronico: str, 
                 fecha_inicio_contrato: date, salario: float):
        self.__id_empleado = id_empleado
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__correo_electronico = correo_electronico
        self.__fecha_inicio_contrato = fecha_inicio_contrato
        self.__salario = salario

    @property
    def id_empleado(self) -> str:
        return self.__id_empleado

    @id_empleado.setter
    def id_empleado(self, valor: str):
        self.__id_empleado = valor

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor

    @property
    def direccion(self) -> str:
        return self.__direccion

    @direccion.setter
    def direccion(self, valor: str):
        self.__direccion = valor

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        self.__telefono = valor

    @property
    def correo_electronico(self) -> str:
        return self.__correo_electronico

    @correo_electronico.setter
    def correo_electronico(self, valor: str):
        if "@" not in valor:
            raise ValueError("Correo electrónico no válido.")
        self.__correo_electronico = valor

    @property
    def fecha_inicio_contrato(self) -> date:
        return self.__fecha_inicio_contrato

    @fecha_inicio_contrato.setter
    def fecha_inicio_contrato(self, valor: date):
        self.__fecha_inicio_contrato = valor

    @property
    def salario(self) -> float:
        return self.__salario

    @salario.setter
    def salario(self, valor: float):
        if valor < 0:
            raise ValueError("El salario no puede ser negativo.")
        self.__salario = valor

    def obtenerInformacion(self) -> dict:
        return {
            "id_empleado": self.__id_empleado,
            "nombre": self.__nombre,
            "direccion": self.__direccion,
            "telefono": self.__telefono,
            "correo_electronico": self.__correo_electronico,
            "fecha_inicio_contrato": str(self.__fecha_inicio_contrato),
            "salario": self.__salario
        }