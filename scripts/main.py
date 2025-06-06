# main.py

from imclib.gestion_datos import (
    crear_archivo_si_no_existe,
    añadir_nuevo_registro,
    ver_registros,
    modificar_registro
)

import os

# === CONFIGURACIÓN DE ARCHIVO ===

ruta_carpeta = "./datos"
os.makedirs(ruta_carpeta, exist_ok=True)

archivo = os.path.join(ruta_carpeta, "resultados_imc.csv")
cabecera = ["Fecha", "Nombre", "Peso", "Altura", "IMC", "Clasificación", "Actividad"]
crear_archivo_si_no_existe(archivo, cabecera)

# === PROGRAMA PRINCIPAL ===

print("=== Calculadora de IMC y Salud ===")
nombre = input("Introduce tu nombre: ")

while True:
    print(f"\nHola {nombre}, ¿qué deseas hacer?")
    print("1. Añadir nuevo registro")
    print("2. Ver registros anteriores")
    print("3. Modificar un registro existente")
    print("4. Salir")

    opcion = input("Selecciona una opción (1-4): ")

    if opcion == "1":
        añadir_nuevo_registro(nombre, archivo)
    elif opcion == "2":
        ver_registros(nombre, archivo)
    elif opcion == "3":
        modificar_registro(nombre, archivo)
    elif opcion == "4":
        print("¡Hasta pronto!")
        break
    else:
        print("Opción no válida. Intenta nuevamente.")



     
# === GLOSARIO DE COMANDOS Y FUNCIONES USADAS ===

# --- Entrada y salida de datos ---
# input() → Solicita datos al usuario desde la consola.
# print() → Muestra información por pantalla.
# f-string → Inserta variables dentro de cadenas de texto: f"Hola {nombre}".
# str.lower() → Convierte un texto a minúsculas para evitar errores al comparar.

# --- Control de flujo ---
# if / elif / else → Ejecutan bloques de código según condiciones.
# while True: → Bucle que se repite indefinidamente hasta que se use break.
# break → Rompe un bucle.
# return → Devuelve un valor desde una función y termina su ejecución.

# --- Conversión de tipos ---
# float() → Convierte un texto o número a decimal (float).
# int() → Convierte un texto o número a entero.

# --- Funciones definidas por el usuario ---
# def nombre_funcion(): → Crea una función personalizada.
# calcular_imc() → Calcula el IMC a partir de peso y altura.
# clasificar_imc() → Clasifica el IMC como "Normal", "Sobrepeso", etc.
# añadir_nuevo_registro(), ver_registros(), modificar_registro() → Agrupan lógica reutilizable.

# --- Manejo de errores ---
# try / except → Ejecuta código y captura errores para evitar que el programa se detenga.

# --- Archivos y carpetas ---
# open("archivo.csv", mode="a") → Abre un archivo para añadir datos.
# mode="w" → Crea o sobreescribe un archivo.
# newline="" → Evita líneas en blanco adicionales al escribir CSVs.
# csv.writer() → Crea un objeto para escribir filas en un archivo CSV.
# os.makedirs(ruta, exist_ok=True) → Crea una carpeta si no existe.
# os.path.exists() → Verifica si existe un archivo o carpeta.
# with open(...) as f: → Abre un archivo de forma segura, se cierra automáticamente.

# --- Fechas ---
# from datetime import datetime → Importa funciones para manejar fechas.
# datetime.today().strftime('%Y-%m-%d') → Devuelve la fecha actual en formato "YYYY-MM-DD".

# --- Pandas ---
# import pandas as pd → Importa la biblioteca pandas.
# pd.read_csv("archivo.csv") → Lee un archivo CSV como tabla (DataFrame).
# df["Columna"] → Accede a una columna del DataFrame.
# df[df["Nombre"] == "Ander"] → Filtra filas por una condición.
# df.to_csv("archivo.csv") → Guarda el DataFrame en un archivo CSV.
# df.at[indice, "Columna"] → Modifica el valor de una celda específica.
# df.loc[indice, ["Col1", "Col2"]] → Accede a varias columnas de una fila.
# df.to_string(index=False) → Muestra el DataFrame sin índice numérico.
