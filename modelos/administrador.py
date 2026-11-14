from .usuario import Usuario

class Administrador(Usuario):
    def __init__(self, username: str, password: str):
        super().__init__(username, password, "administrador")

    def registrar_empleado(self) -> None:
        pass

    def generar_informes(self) -> None:
        pass