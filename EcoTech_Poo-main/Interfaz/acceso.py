import asyncio
from textual.screen import Screen
from textual.containers import Vertical, Center
from textual.widgets import Input, Button, Label, Header, Footer
from Datos.usuario_dao import UsuarioDAO
from modelos.usuario import Usuario

class PantallaLogin(Screen):
    BINDINGS = [("escape", "app.quit", "Salir")]

    def __init__(self):
        super().__init__()
        self.intentos = 0

    def compose(self):
        yield Header(show_clock=True)
        with Center():
            with Vertical(classes="panel-central"):
                yield Label("🔐 CONTROL DE ACCESO", classes="titulo-pantalla")
                yield Input(placeholder="👤 Identificador de usuario", id="in_usr")
                yield Input(placeholder="🔑 Clave de seguridad", password=True, id="in_pwd")
                yield Label("", id="lbl_msg")
                yield Button("🛡️ Autenticar", id="btn_in", variant="success")
                yield Button("📝 Solicitar Acceso (Registro)", id="btn_reg", variant="primary")
        yield Footer()

    async def on_button_pressed(self, event):
        if event.button.id == "btn_reg":
            from Interfaz.acceso import PantallaRegistro
            self.app.push_screen(PantallaRegistro())
            return

        if event.button.id == "btn_in":
            usr = self.query_one("#in_usr").value.strip()
            pwd = self.query_one("#in_pwd").value.strip()
            lbl = self.query_one("#lbl_msg")
            btn = self.query_one("#btn_in")
            
            if not usr or not pwd:
                lbl.styles.color = "#bf616a"
                lbl.update("⚠️ Requerido: Ingrese credenciales.")
                return
            
            try:
                usuario = UsuarioDAO.autenticar(usr, pwd)
                self.intentos = 0
                self.app.usuario_actual = usuario
                from Interfaz.panel import PantallaPanel
                self.app.push_screen(PantallaPanel())
                self.query_one("#in_pwd").value = ""
                lbl.update("")
            except PermissionError:
                self.intentos += 1
                if self.intentos >= 3:
                    lbl.styles.color = "#bf616a"
                    lbl.update("acceso bloqueado")
                    btn.disabled = True
                    
                    await asyncio.sleep(10)
                    
                    self.intentos = 0
                    btn.disabled = False
                    lbl.styles.color = "#a3be8c"
                    lbl.update("sistema restablecido")
                else:
                    faltan = 3 - self.intentos
                    lbl.styles.color = "#bf616a"
                    lbl.update(f"❌ Credenciales inválidas. Intentos: {faltan}.")
            except Exception:
                lbl.styles.color = "#bf616a"
                lbl.update("⚠️ Error de conexión con el servidor.")

class PantallaRegistro(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Cancelar")]

    def compose(self):
        yield Header()
        with Center():
            with Vertical(classes="panel-central"):
                yield Label("📋 REGISTRO DE PERSONAL", classes="titulo-pantalla")
                # Instrucciones claras agregadas directamente en la interfaz
                yield Input(placeholder="👤 Nuevo identificador (3 a 30 caracteres)", id="reg_usr")
                yield Input(placeholder="🔑 Clave de seguridad (Mínimo 8 caracteres)", password=True, id="reg_pwd")
                yield Label("", id="lbl_msg")
                yield Button("✅ Confirmar Registro", id="btn_reg", variant="success")
                yield Button("🔙 Cancelar y Volver", id="btn_volver", variant="primary")
        yield Footer()

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver":
            self.app.pop_screen()
            return
        
        if event.button.id == "btn_reg":
            usr = self.query_one("#reg_usr").value.strip()
            pwd = self.query_one("#reg_pwd").value.strip()
            lbl = self.query_one("#lbl_msg")
            
            if not usr or not pwd:
                lbl.styles.color = "#bf616a"
                lbl.update("⚠️ Requerido: Complete todos los campos.")
                return
            
            try:
                total_usuarios = UsuarioDAO.contar_usuarios()
                rol = "administrador" if total_usuarios == 0 else "empleado"
                nuevo = Usuario(usr, pwd, rol)
                UsuarioDAO.registrar_usuario(nuevo)
                
                lbl.styles.color = "#a3be8c"
                lbl.update(f"✅ Operación exitosa. Privilegios: {rol.upper()}.")
                self.query_one("#reg_usr").value = ""
                self.query_one("#reg_pwd").value = ""
            except ValueError:
                lbl.styles.color = "#bf616a"
                # Mensaje de error fijo mejorado para guiar al usuario
                lbl.update("⚠️ Error: El usuario ya existe o la clave tiene menos de 8 caracteres.")
            except Exception:
                lbl.styles.color = "#bf616a"
                lbl.update("⚠️ Fallo al registrar en la base de datos.")