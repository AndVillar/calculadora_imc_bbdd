from imclib.gestion_datos import (
    crear_archivo_si_no_existe,
    añadir_nuevo_registro,
    ver_registros,
    modificar_registro
)

from imclib.salud import registrar_imc, ver_historial_imc
from imclib.bbdd import inicializar_base_de_datos
from imclib.usuarios import registrar_usuario, ver_usuario, ver_todos_los_usuarios
from imclib.facturas import (
    crear_factura,
    mostrar_facturas_de_usuario,
    mostrar_resumen_financiero
)




import os

# === INICIALIZACIÓN DE BASE DE DATOS ===
inicializar_base_de_datos()

# === CONFIGURACIÓN DE ARCHIVO PARA CSV DE IMC ===
ruta_carpeta = "./datos"
os.makedirs(ruta_carpeta, exist_ok=True)
archivo = os.path.join(ruta_carpeta, "resultados_imc.csv")
cabecera = ["Fecha", "Nombre", "Peso", "Altura", "IMC", "Clasificación", "Actividad"]
crear_archivo_si_no_existe(archivo, cabecera)

# === PROGRAMA PRINCIPAL ===
print("=== CRM + Salud ===")

while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("0. Registrar nuevo usuario")
    print("1. Ver usuario")
    print("2. Ver registros IMC")
    print("3. Crear factura para usuario")
    print("4. Modificar registro IMC")
    print("5. Ver facturas de usuario")
    print("6. Ver resumen financiero")
    print("7. Módulo de Salud (IMC)")
    print("8. Añadir nuevo registro IMC")
    print("9. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "0":
        registrar_usuario()
    elif opcion == "1":
        ver_usuario()
    elif opcion == "2":
        nombre = input("Introduce tu nombre: ")
        ver_registros(nombre, archivo)
    elif opcion == "3":
        crear_factura()
    elif opcion == "4":
        nombre = input("Introduce tu nombre: ")
        modificar_registro(nombre, archivo)
    elif opcion == "5":
        mostrar_facturas_de_usuario()
    elif opcion == "6":
        mostrar_resumen_financiero()
    elif opcion == "7":
        while True:
            print("\n=== MÓDULO DE SALUD ===")
            print("1. Registrar nuevo IMC")
            print("2. Ver historial de IMC")
            print("3. Volver al menú principal")
            subop = input("Elige una opción: ")

            if subop == "1":
                registrar_imc()
            elif subop == "2":
                ver_historial_imc()
            elif subop == "3":
                break
            else:
                print("Opción no válida.")
    elif opcion == "8":
        nombre = input("Introduce tu nombre: ")
        añadir_nuevo_registro(nombre, archivo)
    elif opcion == "9":
        print("¡Hasta pronto!")
        break
    elif opcion == "010":
        while True:
            print("\n=== MENÚ ADMINISTRADOR ===")
            print("1. Ver todos los usuarios")
            print("2. Elimniar usuario (en desarrollo)")
            print("2. Elimniar facturas (en desarrollo)")
            print("5. Salir del modo administrador")

            admin_op = input("Selecciona una opción de admin: ")

            if admin_op == "1":
                ver_todos_los_usuarios()
            elif admin_op == "2":
                print("Saliendo del modo administrador...")
                break
            else:
                print("❌ Opción de administrador no válida.")

    else:
        print("Opción no válida. Intenta nuevamente.")
