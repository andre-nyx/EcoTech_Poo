from .empleado import Empleado

class Departamento:
    def __init__(self, nombre: str, gerente: Empleado = None):
        self.__nombre = nombre
        self.__gerente = gerente          # Relación dirigida "dirigido por"
        self.__empleados = []            # Agregación "agrupa"

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor:
            raise ValueError("El nombre del departamento no puede estar vacío.")
        self.__nombre = valor

    @property
    def gerente(self) -> Empleado:
        return self.__gerente

    def crear(self) -> None:
        pass

    def editar(self) -> None:
        pass

    def buscar(self) -> None:
        pass

    def eliminar(self) -> None:
        pass

    def asignar_empleado(self, e: Empleado) -> None:
        if e not in self.__empleados:
            self.__empleados.append(e)

    def asignar_gerente(self, e: Empleado) -> None:
        self.__gerente = e

    def obtenerInformacion(self) -> dict:
        return {
            "nombre": self.__nombre,
            "gerente": self.__gerente.nombre if self.__gerente else "Sin Gerente",
            "total_empleados": len(self.__empleados)
        }
