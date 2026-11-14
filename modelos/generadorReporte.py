from abc import ABC, abstractmethod

class GeneradorReporte(ABC):
    @abstractmethod
    def exportar_datos(self) -> None:
        pass