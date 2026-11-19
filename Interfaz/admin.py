from textual.screen import Screen
from textual.containers import Vertical, Center
from textual.widgets import DataTable, Button, Label, Input, Header, Footer
from Datos.usuario_dao import UsuarioDAO

class PantallaAdmin(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Volver al Dashboard")]

    def compose(self):
        yield Header()
        with Center():
            with Vertical(classes="panel-central"):
                yield Label("🛠️ CONSOLA DE ADMINISTRACIÓN", classes="titulo-pantalla")
                yield DataTable(id="tabla_usr")
                
                yield Input(placeholder="🎯 Identificador de usuario objetivo", id="in_target")
                
                yield Button("🔄 Actualizar Privilegios (Admin / Empleado)", id="btn_rol", variant="warning")
                yield Button("🚫 Revocar Acceso y Eliminar Cuenta", id="btn_eliminar", variant="error")
                
                yield Label("", id="lbl_msg")
                yield Button("🔙 Retornar al Dashboard", id="btn_volver", variant="primary")
        yield Footer()

    def on_mount(self):
        tabla = self.query_one(DataTable)
        tabla.add_columns("IDENTIFICADOR", "NIVEL DE PRIVILEGIO")
        self.cargar_datos()

    def cargar_datos(self):
        tabla = self.query_one(DataTable)
        tabla.clear()
        try:
            for usr, rol in UsuarioDAO.listar_usuarios():
                tabla.add_row(usr, rol.upper())
        except Exception:
            self.query_one("#lbl_msg").update("⚠️ Error de sincronización con base de datos.")

    def on_button_pressed(self, event):
        if event.button.id == "btn_volver":
            self.app.pop_screen()
            return

        target = self.query_one("#in_target").value.strip()
        lbl = self.query_one("#lbl_msg")
        mi_usuario = self.app.usuario_actual.username

        if not target:
            lbl.update("⚠️ Requerido: Indique un identificador válido.")
            return
            
        # CORRECCIÓN DE SEGURIDAD: Convertimos ambos a minúsculas para comparar
        if target.lower() == mi_usuario.lower():
            lbl.update("🛑 Operación denegada: Violación de política de seguridad (Auto-modificación).")
            return

        try:
            if event.button.id == "btn_eliminar":
                UsuarioDAO.eliminar_usuario(target)
                lbl.update(f"✅ Registro '{target}' eliminado permanentemente.")
                self.cargar_datos()
                
            elif event.button.id == "btn_rol":
                # Convertimos las llaves del diccionario a minúsculas para hacer una búsqueda segura
                usuarios = {k.lower(): v for k, v in UsuarioDAO.listar_usuarios()}
                
                if target.lower() not in usuarios:
                    lbl.update("⚠️ Identificador no localizado en el sistema.")
                    return
                
                nuevo_rol = "administrador" if usuarios[target.lower()] == "empleado" else "empleado"
                UsuarioDAO.actualizar_rol(target, nuevo_rol)
                lbl.update(f"✅ Privilegios de '{target}' modificados a {nuevo_rol.upper()}.")
                self.cargar_datos()
        except Exception:
            lbl.update("⚠️ Excepción interna al escribir en MySQL.")