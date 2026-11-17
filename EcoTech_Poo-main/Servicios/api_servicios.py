import os
import re
from pathlib import Path

import requests

_PATRON_CIUDAD = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' .-]{2,60}(,\s?[A-Za-z]{2})?")


def cargar_env():
    """Lee el archivo .env local si existe para cargar la API Key de forma segura."""
    ruta_env = Path(__file__).resolve().parent.parent / ".env"
    if ruta_env.exists():
        with open(ruta_env, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea and not linea.startswith("#") and "=" in linea:
                    clave, valor = linea.split("=", 1)
                    os.environ[clave.strip()] = valor.strip()


cargar_env()


class APIservice:
    """
    Capa de Servicio: Se encarga exclusivamente de la comunicacion con APIs
    externas.
    """

    @staticmethod
    def obtener_indicadores():
        """
        Consulta los indicadores economicos (Dólar, Euro, UF, UTM, IPC) desde la API 
        findic.cl
        Si ocurre un error de red o servidor, lanza una excepcion real (raise).
        """
        url = "https://findic.cl/api/"
        headers = {
            "User-Agent": "EcoTechSystem/1.0",
            "Accept": "application/json"
        }

        try:
            # Petición HTTP con tiempo de espera de 5 segundos
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()

            datos = response.json()

            return {
                "dolar": datos.get("dolar", {}).get("valor"),
                "euro": datos.get("euro", {}).get("valor"),
                "uf": datos.get("uf", {}).get("valor"),
                "utm": datos.get("utm", {}).get("valor"),
                "ipc": datos.get("ipc", {}).get("valor")
            }

        except requests.exceptions.Timeout:
            raise ConnectionError("Tiempo de espera agotado al conectar con la API de indicadores.") from None

        except requests.exceptions.HTTPError as http_err:
            codigo = http_err.response.status_code if http_err.response is not None else "desconocido"
            raise ConnectionError(f"Error en el servidor externo de indicadores (Código HTTP {codigo}).") from None

        except (ValueError, KeyError, IndexError, TypeError, AttributeError):
            raise ValueError("Los datos recibidos de la API económica no tienen el formato esperado.") from None

        except requests.exceptions.RequestException:
            raise ConnectionError("No hay conexión a internet o el servidor de indicadores no está disponible.") from None

    @staticmethod
    def obtener_clima(ciudad: str):
        """
        Consulta temperatura, humedad y estado del tiempo desde OpenWeatherMap.
        Valida la entrada del usuario y protege la API Key.
        """
        # 1. Validación de entrada 
        if not isinstance(ciudad, str) or not _PATRON_CIUDAD.fullmatch(ciudad.strip()):
            raise ValueError("Ingrese una ciudad válida (solo letras, espacios y guion; opcional ', CL').")

        # Seguridad 
        api_key = os.getenv("OPENWEATHER_API_KEY", "")
        if not api_key:
            raise ConnectionError("Falta configurar la API Key de OpenWeatherMap en el archivo .env.")

        url = "https://api.openweathermap.org/data/2.5/weather"

        parametros = {
            "q": ciudad.strip(),
            "appid": api_key,
            "units": "metric",  # Grados Celsius
            "lang": "es"        # Descripción en español
        }

        try:
            response = requests.get(url, params=parametros, timeout=5)
            response.raise_for_status()
            datos = response.json()

            return {
                "ciudad": datos.get("name", ciudad.strip()),
                "temperatura": datos["main"]["temp"],
                "humedad": datos["main"]["humidity"],
                "estado": datos["weather"][0]["description"].capitalize()
            }

        except requests.exceptions.Timeout:
            raise ConnectionError("Tiempo de espera agotado al conectar con el servicio de clima.") from None

        except requests.exceptions.HTTPError as http_err:
            codigo = http_err.response.status_code if http_err.response is not None else "desconocido"
            if codigo == 401:
                raise ConnectionError("Error de autenticación con la API de clima (API Key inválida o aún en activación).") from None
            elif codigo == 404:
                raise ValueError(f"No se encontró información climática para la ciudad '{ciudad}'.") from None
            else:

                raise ConnectionError(f"Error en el servidor de clima (Código HTTP {codigo}).") from None

        except (ValueError, KeyError, IndexError, TypeError, AttributeError):
            raise ValueError("Error al procesar la respuesta del servicio de clima.") from None

        except requests.exceptions.RequestException:
            raise ConnectionError("No hay conexión a internet o el servidor de clima no está disponible.") from None