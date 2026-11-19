import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from textual.app import App
from Interfaz.acceso import PantallaLogin

class EcoTechApp(App):
    TITLE = "EcoTech Solutions"
    
    CSS = """
    Screen {
        background: #1e1e2e;
        align: center middle;
    }
    Header {
        background: #2e3440;
        color: #eceff4;
    }
    Footer {
        background: #2e3440;
    }
    .panel-central {
        width: 55;
        height: auto;
        padding: 1 3;
        border: round #4c566a;
        background: #282a36;
        margin: 1;
    }
    .titulo-pantalla {
        content-align: center middle;
        text-style: bold;
        color: #eceff4;
        background: #3b4252;
        width: 100%;
        padding: 1;
        margin-bottom: 2;
    }
    Input {
        border: tall #434c5e;
        background: #1e1e2e;
        margin-bottom: 1;
    }
    Input:focus {
        border: tall #81a1c1;
    }
    Button {
        width: 100%;
        margin-bottom: 1;
        text-style: bold;
    }
    Button.-success {
        background: #5e81ac;
        color: white;
    }
    Button.-primary {
        background: #434c5e;
        color: white;
    }
    /* ESTO PONE EL BOTÓN GRIS CUANDO SE BLOQUEA */
    Button:disabled {
        background: #555555; 
        color: #888888;
        border: none;
    }
    #lbl_msg {
        content-align: center middle;
        text-style: bold;
        color: #bf616a;
        margin-bottom: 1;
        width: 100%;
    }
    """

    def on_mount(self) -> None:
        self.usuario_actual = None
        self.push_screen(PantallaLogin())

if __name__ == "__main__":
    app = EcoTechApp()
    app.run()