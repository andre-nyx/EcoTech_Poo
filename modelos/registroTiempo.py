from datetime import date
from .proyecto import Proyecto
from .empleado import Empleado
    

class RegistroTiempo:
    def __init__(self, fecha: date, horas_trabajadas: float, descripcion_tareas: str, 
                 empleado: Empleado = None, proyecto: Proyecto = None):
        self.__fecha = fecha
        self.__horas_trabajadas = horas_trabajadas
        self.__descripcion_tareas = descripcion_tareas
        self.__empleado = empleado        # Relación "Realiza"
        self.__proyecto = proyecto        # Relación "asocia"

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, valor: date):
        self.__fecha = valor

    @property
    def horas_trabajadas(self) -> float:
        return self.__horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, valor: float):
        if valor < 0:
            raise ValueError("Las horas trabajadas no pueden ser negativas.")
        self.__horas_trabajadas = valor

    @property
    def descripcion_tareas(self) -> str:
        return self.__descripcion_tareas

    @descripcion_tareas.setter
    def descripcion_tareas(self, valor: str):
        self.__descripcion_tareas = valor

    def registrar(self) -> None:
        pass

    def obtenerInformacion(self) -> dict:
        return {
            "fecha": str(self.__fecha),
            "horas_trabajadas": self.__horas_trabajadas,
            "descripcion_tareas": self.__descripcion_tareas,
            "empleado": self.__empleado.nombre if self.__empleado else "Sin asignar",
            "proyecto": self.__proyecto.nombre if self.__proyecto else "Sin asignar"
        }