from textual.screen import Screen
from textual.containers import Vertical, Center
from textual.widgets import Label, Button, Select, Input, Header, Footer
from Servicios.api_servicios import APIservice

class PantallaPanel(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Cerrar Sesión")]

    def compose(self):
        yield Header(show_clock=True)
        with Center():
            with Vertical(classes="panel-central"):
                yield Label("", id="titulo_panel", classes="titulo-pantalla")
                yield Label("⏳ Sincronizando datos de mercado...", id="lbl_indicadores")
                
                yield Input(placeholder="💵 Monto a liquidar (CLP)", id="in_monto")
                yield Button("💱 Procesar Equivalencia de Divisas", id="btn_conversion", variant="success")
                yield Label("", id="lbl_conversion")
                
                ciudades = [
                    ("Santiago", "Santiago, CL"), 
                    ("Copiapó", "Copiapo, CL"), 
                    ("Antofagasta", "Antofagasta, CL"), 
                    ("Concepción", "Concepcion, CL")
                ]
                yield Select(ciudades, prompt="📍 Seleccione base operativa", id="sel_ciudad")
                yield Button("🌍 Ejecutar Consulta Meteorológica", id="btn_clima", variant="success")
                yield Label("", id="lbl_clima")
                
                yield Button("⚙️ Módulo de Administración", id="btn_admin", variant="warning")
                yield Button("🚪 Finalizar Sesión", id="btn_salir", variant="primary")
        yield Footer()

    def on_mount(self):
        usr = self.app.usuario_actual
        if usr:
            self.query_one("#titulo_panel").update(f"📊 DASHBOARD OPERATIVO | {usr.username.upper()} [{usr.rol.upper()}]")
            if usr.rol != "administrador":
                self.query_one("#btn_admin").display = False
        
        try:
            datos = APIservice.obtener_indicadores()
            texto = f"💹 MERCADO | USD: ${datos.get('dolar')} | EUR: ${datos.get('euro')} | UF: ${datos.get('uf')}"
            self.query_one("#lbl_indicadores").update(texto)
            self.datos_api = datos
        except Exception:
            self.query_one("#lbl_indicadores").update("⚠️ Servicio de mercado temporalmente inactivo.")
            self.datos_api = None

    def on_button_pressed(self, event):
        if event.button.id == "btn_salir":
            self.app.usuario_actual = None
            self.app.pop_screen()
        elif event.button.id == "btn_admin":
            from Interfaz.admin import PantallaAdmin
            self.app.push_screen(PantallaAdmin())
        elif event.button.id == "btn_conversion":
            self.calcular_conversion()
        elif event.button.id == "btn_clima":
            self.consultar_clima()

    def calcular_conversion(self):
        lbl = self.query_one("#lbl_conversion")
        monto_str = self.query_one("#in_monto").value.strip()
        if not self.datos_api or not self.datos_api.get("dolar"):
            lbl.update("⚠️ Error: Tasas de conversión no sincronizadas.")
            return
        try:
            monto = float(monto_str)
            if monto <= 0: raise ValueError
            usd = monto / self.datos_api["dolar"]
            eur = monto / self.datos_api["euro"]
            lbl.update(f"✅ LIQUIDACIÓN: ${usd:,.2f} USD | €{eur:,.2f} EUR")
        except ValueError:
            lbl.update("⚠️ Rechazado: Ingrese un formato numérico válido.")
    
    def consultar_clima(self):
        lbl = self.query_one("#lbl_clima")
        sel = self.query_one("#sel_ciudad").value
        if sel == Select.BLANK:
            lbl.update("⚠️ Requerido: Seleccione una zona operativa de la lista.")
            return
        try:
            clima = APIservice.obtener_clima(sel)
            lbl.update(f"🌤️ REPORTE {clima['ciudad'].upper()}: {clima['temperatura']}°C | {clima['humedad']}% Hum. | {clima['estado'].upper()}")
        except Exception:
            lbl.update("⚠️ Fallo al contactar servicio meteorológico externo.")