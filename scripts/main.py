from imclib.gestion_datos import (
    crear_archivo_si_no_existe,
    añadir_nuevo_registro,
    ver_registros,
    modificar_registro
)

from imclib.bbdd import inicializar_base_de_datos
from imclib.usuarios import registrar_usuario

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
    print("1. Añadir nuevo registro IMC")
    print("2. Ver registros IMC")
    print("3. Modificar registro IMC")
    print("4. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "0":
        registrar_usuario()
    elif opcion == "1":
        nombre = input("Introduce tu nombre: ")
        añadir_nuevo_registro(nombre, archivo)
    elif opcion == "2":
        nombre = input("Introduce tu nombre: ")
        ver_registros(nombre, archivo)
    elif opcion == "3":
        nombre = input("Introduce tu nombre: ")
        modificar_registro(nombre, archivo)
    elif opcion == "4":
        print("¡Hasta pronto!")
        break
    else:
        print("Opción no válida. Intenta nuevamente.")
