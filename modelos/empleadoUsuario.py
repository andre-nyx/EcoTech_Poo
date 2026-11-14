from .usuario import Usuario

class EmpleadoUsuario(Usuario):
    def __init__(self, username: str, password: str, empleado=None):
        super().__init__(username, password, "empleado")
        self.__empleado = empleado

    @property
    def empleado(self):
        return self.__empleado

    @empleado.setter
    def empleado(self, valor):
        self.__empleado = valor

    def registrar_horas(self) -> None:
        pass