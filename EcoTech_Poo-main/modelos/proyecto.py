from datetime import date
from .empleado import Empleado

class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fecha_inicio: date):
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
        self.__empleados_asignados = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor:
            raise ValueError("El nombre del proyecto no puede estar vacío.")
        self.__nombre = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str):
        self.__descripcion = valor

    @property
    def fecha_inicio(self) -> date:
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor: date):
        if not valor:
            raise ValueError("La fecha de inicio no puede estar vacía.")
        self.__fecha_inicio = valor

    def crear(self) -> None:
        pass

    def editar(self) -> None:
        pass

    def eliminar(self) -> None:
        pass

    def asignar_empleado(self, e: Empleado) -> None:
        if e not in self.__empleados_asignados:
            self.__empleados_asignados.append(e)

    def obtenerInformacion(self) -> dict:
        return {
            "nombre": self.__nombre,
            "descripcion": self.__descripcion,
            "fecha_inicio": str(self.__fecha_inicio),
            "empleados_asignados": len(self.__empleados_asignados)
        }

