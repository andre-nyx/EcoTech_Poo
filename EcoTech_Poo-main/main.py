import getpass
import math
import sys
import time

from Datos.setup_bd import inicializar_bd
from Datos.usuario_dao import UsuarioDAO
from modelos.usuario import Usuario
from Servicios.api_servicios import APIservice

MENSAJE_INESPERADO = "Ocurrió un problema inesperado. Intente nuevamente."
MAX_INTENTOS = 3
ESPERA_SEGUNDOS = 10


# ---------------------------------------------------------------- MENÚS
def menu_sesion():
    print("\n" + "=" * 50)
    print("      ECOTECH SOLUTIONS - ACCESO SEGURO")
    print("=" * 50)
    print("1. Iniciar Sesión")
    print("2. Registrarse")
    print("3. Salir")
    return input("Seleccione una opción (1-3): ").strip()


def menu_operativo(usuario: Usuario):
    print("\n" + "=" * 50)
    print(f"  PANEL OPERATIVO ECOTECH - USUARIO: {usuario.username.upper()}")
    print(f"  ROL: {usuario.rol.upper()} | ESTADO: SESIÓN ACTIVA")
    print("=" * 50)
    print("1. Consultar Indicadores Económicos (API en Vivo)")
    print("2. Simular Conversión de Pago Internacional (Divisas)")
    print("3. Consultar Clima para Planificación de Proyectos (API en Vivo)")
    print("4. Cerrar Sesión")
    if usuario.rol == "administrador":
        print("5. Administrar Usuarios (solo administradores)")
    return input("Seleccione una opción: ").strip()


def menu_admin():
    print("\n--- ADMINISTRACIÓN DE USUARIOS ---")
    print("1. Listar Usuarios Registrados")
    print("2. Cambiar Rol de Usuario")
    print("3. Eliminar Usuario")
    print("4. Volver")
    return input("Seleccione una opción (1-4): ").strip()


# ------------------------------------------------- ACCESO (sin sesión)
def flujo_registro():
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    username = input("Ingrese nombre de usuario (3-30 caracteres): ").strip()
    password = getpass.getpass("Ingrese contraseña (mínimo 8 caracteres, oculta): ")
    confirmacion = getpass.getpass("Repita la contraseña: ")

    try:
        if password != confirmacion:
            raise ValueError("Las contraseñas no coinciden.")
        # El primer usuario del sistema es administrador; el resto, empleados.
        rol = "administrador" if UsuarioDAO.contar_usuarios() == 0 else "empleado"
        nuevo_usuario = Usuario(username=username, password=password, rol=rol)
        UsuarioDAO.registrar_usuario(nuevo_usuario)
        print(f"\n[ÉXITO] Usuario '{username}' registrado como '{rol.upper()}'.")
    except (ValueError, ConnectionError) as err:
        print(f"\n[ERROR DE REGISTRO]: {err}")
    except Exception:
        print(f"\n[ERROR INESPERADO]: {MENSAJE_INESPERADO}")


def flujo_login():
    print("\n--- AUTENTICACIÓN DE CREDENCIALES ---")
    username = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña (oculta al escribir): ")

    try:
        usuario_autenticado = UsuarioDAO.autenticar(username, password)
        usuario_autenticado.acceder_modulo()
        print(f"\n[ÉXITO] Autenticación completada. ¡Bienvenido(a), {usuario_autenticado.username}!")
        return usuario_autenticado
    except (ValueError, PermissionError, ConnectionError) as err:
        print(f"\n[ACCESO DENEGADO]: {err}")
        return None
    except Exception:
        print(f"\n[ERROR CRÍTICO]: {MENSAJE_INESPERADO}")
        return None


# ------------------------------------------ ADMINISTRACIÓN (solo admin)
def flujo_listar_usuarios():
    print("\n--- REGISTRO DE USUARIOS EN EL SISTEMA ---")
    try:
        usuarios = UsuarioDAO.listar_usuarios()
        if not usuarios:
            print("[INFO] No hay usuarios registrados en el sistema.")
            return

        print(f"Total de usuarios registrados: {len(usuarios)}")
        print("-" * 45)
        print(f"{'N°':<4} | {'NOMBRE DE USUARIO':<22} | {'ROL':<12}")
        print("-" * 45)
        for i, (nombre, rol) in enumerate(usuarios, start=1):
            print(f"{i:<4} | {nombre:<22} | {rol.upper():<12}")
        print("-" * 45)
    except ConnectionError as err:
        print(f"\n[ERROR DE CONEXIÓN]: {err}")
    except Exception:
        print(f"\n[ERROR INESPERADO]: {MENSAJE_INESPERADO}")


def flujo_modificar_rol(admin: Usuario):
    print("\n--- MODIFICAR ROL DE USUARIO ---")
    username = input("Ingrese el nombre de usuario al que desea cambiar el rol: ").strip()
    if username == admin.username:
        print("\n[CANCELADO]: No puede cambiar su propio rol.")
        return

    print("\nSeleccione el nuevo rol:")
    print("1. Empleado")
    print("2. Administrador")
    opcion = input("Opción (1 o 2): ").strip()

    if opcion == "1":
        nuevo_rol = "empleado"
    elif opcion == "2":
        nuevo_rol = "administrador"
    else:
        print("\n[CANCELADO]: Opción no válida.")
        return

    try:
        UsuarioDAO.actualizar_rol(username, nuevo_rol)
        print(f"\n[ÉXITO]: El rol de '{username}' fue actualizado a '{nuevo_rol.upper()}'.")
    except (ValueError, ConnectionError) as err:
        print(f"\n[ERROR]: {err}")
    except Exception:
        print(f"\n[ERROR INESPERADO]: {MENSAJE_INESPERADO}")


def flujo_eliminar(admin: Usuario):
    print("\n--- ELIMINACIÓN DE USUARIO ---")
    username = input("Ingrese el nombre de usuario a eliminar: ").strip()
    if username == admin.username:
        print("\n[CANCELADO]: No puede eliminar su propia cuenta.")
        return
    confirmacion = input(f"¿Confirmas eliminar a '{username}'? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("\n[CANCELADO] No se eliminó el usuario.")
        return

    try:
        UsuarioDAO.eliminar_usuario(username)
        print(f"\n[ÉXITO] Usuario '{username}' eliminado.")
    except (ValueError, ConnectionError) as err:
        print(f"\n[ERROR]: {err}")
    except Exception:
        print(f"\n[ERROR INESPERADO]: {MENSAJE_INESPERADO}")


def flujo_administracion(usuario: Usuario):
    while True:
        # Se vuelve a exigir el rol en cada acción, no solo al entrar al menú.
        usuario.exigir_rol("administrador")
        opcion = menu_admin()
        if opcion == "1":
            flujo_listar_usuarios()
        elif opcion == "2":
            flujo_modificar_rol(usuario)
        elif opcion == "3":
            flujo_eliminar(usuario)
        elif opcion == "4":
            return
        else:
            print("\nOpción no válida.")


# ------------------------------------------- FUNCIONES CON SESIÓN
def flujo_indicadores(usuario: Usuario):
    usuario.acceder_modulo()
    print("\nConectando con el servicio de indicadores externos...")
    try:
        datos = APIservice.obtener_indicadores()
        print("\n--- INDICADORES ECONÓMICOS ACTUALES (findic.cl) ---")
        print(f"   • Dólar Observado : ${datos['dolar']:.2f} CLP" if datos['dolar'] else "   • Dólar: No disponible")
        print(f"   • Euro Oficial    : ${datos['euro']:.2f} CLP" if datos['euro'] else "   • Euro: No disponible")
        print(f"   • UF              : ${datos['uf']:.2f} CLP" if datos['uf'] else "   • UF: No disponible")
        print(f"   • UTM             : ${datos['utm']:.2f} CLP" if datos['utm'] else "   • UTM: No disponible")
    except ConnectionError as err:
        print(f"\n[FALLA EN SERVICIO EXTERNO]: {err}")
    except Exception:
        print(f"\n[ERROR EN CONSUMO API]: {MENSAJE_INESPERADO}")


def flujo_conversion(usuario: Usuario):
    usuario.acceder_modulo()
    print("\n--- CÁLCULO DE PAGO INTERNACIONAL ---")
    monto_str = input("Ingrese el monto del sueldo en CLP: ").strip()

    try:
        try:
            monto_clp = float(monto_str)
        except ValueError:
            raise ValueError("El monto debe ser un número (ejemplo: 450000).") from None
        if not math.isfinite(monto_clp) or monto_clp <= 0 or monto_clp > 1_000_000_000:
            raise ValueError("El monto debe ser un número positivo y razonable.")

        datos = APIservice.obtener_indicadores()
        valor_dolar = datos.get("dolar")
        valor_euro = datos.get("euro")

        if not valor_dolar or not valor_euro:
            raise ConnectionError("No se pudieron obtener las tasas de cambio de la API externa.")

        pago_usd = monto_clp / valor_dolar
        pago_eur = monto_clp / valor_euro

        print("\nResultados calculados en tiempo real:")
        print(f"   -> Equivalente en Dólares (USD) : ${pago_usd:,.2f} USD (Tasa: ${valor_dolar})")
        print(f"   -> Equivalente en Euros (EUR)   : €{pago_eur:,.2f} EUR (Tasa: ${valor_euro})")

    except ValueError as err:
        print(f"\n[DATO INVÁLIDO]: {err}")
    except ConnectionError as err:
        print(f"\n[FALLA DE RED/API]: {err}")
    except Exception:
        print(f"\n[ERROR INESPERADO]: {MENSAJE_INESPERADO}")


def flujo_clima(usuario: Usuario):
    usuario.acceder_modulo()
    print("\n--- CONSULTA CLIMÁTICA DE PROYECTOS ---")
    ciudad = input("Ingrese la ciudad donde se ejecuta el proyecto (ej. Copiapo, Santiago): ").strip()
    print("Conectando con el servicio meteorológico...")

    try:
        clima = APIservice.obtener_clima(ciudad)
        print(f"\n--- CONDICIONES CLIMÁTICAS EN {clima['ciudad'].upper()} ---")
        print(f"   • Temperatura : {clima['temperatura']} °C")
        print(f"   • Humedad     : {clima['humedad']}%")
        print(f"   • Estado      : {clima['estado']}")
    except ValueError as err:
        print(f"\n[DATO INVÁLIDO]: {err}")
    except ConnectionError as err:
        print(f"\n[FALLA EN SERVICIO EXTERNO]: {err}")
    except Exception:
        print(f"\n[ERROR EN CONSUMO API]: {MENSAJE_INESPERADO}")


def sesion_operativa(usuario: Usuario):
    while True:
        opcion = menu_operativo(usuario)
        try:
            if opcion == "1":
                flujo_indicadores(usuario)
            elif opcion == "2":
                flujo_conversion(usuario)
            elif opcion == "3":
                flujo_clima(usuario)
            elif opcion == "4":
                print(f"\nCerrando sesión de {usuario.username}.")
                return
            elif opcion == "5":
                flujo_administracion(usuario)
            else:
                print("\nOpción no válida.")
        except PermissionError as err:
            print(f"\n[ACCESO DENEGADO]: {err}")


# ------------------------------------------------------------ PRINCIPAL
def main():
    try:
        inicializar_bd()
    except ConnectionError as err:
        print(f"[ADVERTENCIA BD]: {err}")
    except Exception:
        print(f"[ADVERTENCIA BD]: {MENSAJE_INESPERADO}")

    intentos_fallidos = 0
    while True:
        opcion = menu_sesion()

        if opcion == "1":
            usuario_actual = flujo_login()
            if usuario_actual is None:
                intentos_fallidos += 1
                if intentos_fallidos >= MAX_INTENTOS:
                    print(f"\n[BLOQUEO TEMPORAL]: Demasiados intentos fallidos. "
                          f"Espere {ESPERA_SEGUNDOS} segundos.")
                    time.sleep(ESPERA_SEGUNDOS)
                    intentos_fallidos = 0
                continue
            intentos_fallidos = 0
            sesion_operativa(usuario_actual)
        elif opcion == "2":
            flujo_registro()
        elif opcion == "3":
            print("\nSaliendo de EcoTech Solutions.")
            sys.exit(0)
        else:
            print("\nOpción inválida. Seleccione entre 1 y 3.")


if __name__ == "__main__":
    main()