import sys
import getpass
from Datos.setup_bd import inicializar_bd
from Datos.usuario_dao import UsuarioDAO
from modelos.usuario import Usuario
from Servicios.api_servicios import APIservice


def menu_sesion():
    print("\n" + "="*50)
    print("      ECOTECH SOLUTIONS - ACCESO SEGURO")
    print("="*50)
    print("1. Iniciar Sesión")
    print("2. Registrar Nuevo Usuario")
    print("3. Listar Usuarios Registrados")
    print("4. Cambiar Rol de Usuario")
    print("5. Eliminar Usuario")
    print("6. Salir")
    return input("Seleccione una opción (1-6): ").strip()


def menu_operativo(usuario: Usuario):
    print("\n" + "="*50)
    print(f"  PANEL OPERATIVO ECOTECH - USUARIO: {usuario.username.upper()}")
    print(f"  ROL: {usuario.rol.upper()} | ESTADO: SESIÓN ACTIVA")
    print("="*50)
    print("1. Consultar Indicadores Económicos (API en Vivo)")
    print("2. Simular Conversión de Pago Internacional (Divisas)")
    print("3. Consultar Clima para Planificación de Proyectos (API en Vivo)")
    print("4. Cerrar Sesión")
    return input("Seleccione una opción (1-4): ").strip()


def flujo_registro():
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    username = input("Ingrese nombre de usuario (3-30 caracteres): ").strip()
    password = input("Ingrese contraseña (visible, mínimo 8 caracteres): ").strip()
    
    print("\nSeleccione el rol del usuario:")
    print("1. Empleado")
    print("2. Administrador")
    opcion_rol = input("Opción (1 o 2) [por defecto 1]: ").strip()
    rol = "administrador" if opcion_rol == "2" else "empleado"

    try:
        nuevo_usuario = Usuario(username=username, password=password, rol=rol)
        UsuarioDAO.registrar_usuario(nuevo_usuario)
        print(f"\n[ÉXITO] Usuario '{username}' registrado como '{rol.upper()}' con credencial cifrada en MySQL.")
    except (ValueError, ConnectionError) as err:
        print(f"\n[ERROR DE REGISTRO]: {err}")
    except Exception as err:
        print(f"\n[ERROR INESPERADO]: No fue posible registrar al usuario. Detalle: {err}")


def flujo_listar_usuarios():
    print("\n--- REGISTRO DE USUARIOS EN EL SISTEMA ---")
    try:
        usuarios = UsuarioDAO.listar_usuarios()
        if not usuarios:
            print("[INFO] No hay usuarios registrados en el sistema.")
            return

        total = len(usuarios)
        print(f"Total de usuarios registrados: {total}")
        print("-" * 45)
        print(f"{'N°':<4} | {'NOMBRE DE USUARIO':<22} | {'ROL':<12}")
        print("-" * 45)
        for i, (nombre, rol) in enumerate(usuarios, start=1):
            print(f"{i:<4} | {nombre:<22} | {rol.upper():<12}")
        print("-" * 45)
    except ConnectionError as err:
        print(f"\n[ERROR DE CONEXIÓN]: {err}")
    except Exception as err:
        print(f"\n[ERROR INESPERADO]: {err}")


def flujo_login() -> Usuario:
    print("\n--- AUTENTICACIÓN DE CREDENCIALES ---")
    username = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña (oculta al escribir): ").strip()

    try:
        usuario_autenticado = UsuarioDAO.autenticar(username, password)
        usuario_autenticado.acceder_modulo()
        print(f"\n[ÉXITO] Autenticación completada. ¡Bienvenido(a), {usuario_autenticado.username}!")
        return usuario_autenticado
    except (ValueError, PermissionError, ConnectionError) as err:
        print(f"\n[ACCESO DENEGADO]: {err}")
        return None
    except Exception as err:
        print(f"\n[ERROR CRÍTICO]: Falla interna al validar credenciales: {err}")
        return None


def flujo_modificar_rol():
    print("\n--- MODIFICAR ROL DE USUARIO ---")
    username = input("Ingrese el nombre de usuario al que desea cambiar el rol: ").strip()
    
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
        print(f"\n[ÉXITO]: El rol de '{username}' fue actualizado a '{nuevo_rol.upper()}' en MySQL.")
    except (ValueError, ConnectionError) as err:
        print(f"\n[ERROR]: {err}")
    except Exception as err:
        print(f"\n[ERROR INESPERADO]: {err}")


def flujo_eliminar():
    print("\n--- ELIMINACIÓN DE USUARIO ---")
    username = input("Ingrese el nombre de usuario a eliminar: ").strip()
    confirmacion = input(f"¿Confirmas eliminar a '{username}'? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("\n[CANCELADO] No se eliminó el usuario.")
        return

    try:
        UsuarioDAO.eliminar_usuario(username)
        print(f"\n[ÉXITO] Usuario '{username}' eliminado de MySQL.")
    except (ValueError, ConnectionError) as err:
        print(f"\n[ERROR]: {err}")
    except Exception as err:
        print(f"\n[ERROR INESPERADO]: {err}")


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
    except Exception as err:
        print(f"\n[ERROR EN CONSUMO API]: {err}")


def flujo_conversion(usuario: Usuario):
    usuario.acceder_modulo()
    print("\n--- CÁLCULO DE PAGO INTERNACIONAL ---")
    monto_str = input("Ingrese el monto del sueldo en CLP: ").strip()
    
    try:
        monto_clp = float(monto_str)
        if monto_clp <= 0:
            raise ValueError("El monto debe ser un valor positivo.")
        
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
    except Exception as err:
        print(f"\n[ERROR INESPERADO]: {err}")


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
    except Exception as err:
        print(f"\n[ERROR EN CONSUMO API]: {err}")


def main():
    try:
        inicializar_bd()
    except Exception as err:
        print(f"[ADVERTENCIA BD]: {err}")

    while True:
        opcion = menu_sesion()

        if opcion == "1":
            usuario_actual = flujo_login()
            if usuario_actual:
                while True:
                    sub_opcion = menu_operativo(usuario_actual)
                    if sub_opcion == "1":
                        flujo_indicadores(usuario_actual)
                    elif sub_opcion == "2":
                        flujo_conversion(usuario_actual)
                    elif sub_opcion == "3":
                        flujo_clima(usuario_actual)
                    elif sub_opcion == "4":
                        print(f"\nCerrando sesión de {usuario_actual.username}.")
                        break
                    else:
                        print("\nOpción no válida.")
        elif opcion == "2":
            flujo_registro()
        elif opcion == "3":
            flujo_listar_usuarios()
        elif opcion == "4":
            flujo_modificar_rol()
        elif opcion == "5":
            flujo_eliminar()
        elif opcion == "6":
            print("\nSaliendo de EcoTech Solutions.")
            sys.exit(0)
        else:
            print("\nOpción inválida. Seleccione entre 1 y 6.")


if __name__ == "__main__":
    main()