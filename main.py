from datetime import datetime
import csv
import os
import pandas as pd
from os.path import exists


# Proyecto: Calculadora de IMC - Ander Villar - Master IA y Data Science


# === FUNCIONES ===

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def clasificar_imc(imc): 
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

def crear_archivo_si_no_existe(archivo, cabecera):
    if not os.path.exists(archivo):
        with open(archivo, mode="w", newline="", encoding="latin1") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(cabecera)

def añadir_nuevo_registro(nombre, archivo):
    try:
        peso = float(input("Introduce tu peso en kilogramos (ej: 70): "))
        altura = float(input("Introduce tu altura en metros (ej: 1.75): "))
        actividad = input("¿Cuál es tu nivel de actividad física? (bajo/medio/alto): ").lower()
        fecha_actual = datetime.today().strftime('%Y-%m-%d')

        # Leer CSV para comprobar duplicados
        if os.path.exists(archivo):
            df = pd.read_csv(archivo, encoding="latin1", sep=";")
            existe = ((df["Nombre"] == nombre) & (df["Fecha"] == fecha_actual)).any()
            if existe:
                print(f"\n Ya existe un registro para {nombre} en la fecha {fecha_actual}. No se añadirá otro.")
                return

        imc = calcular_imc(peso, altura)
        clasificacion = clasificar_imc(imc)

        print(f"\n{nombre}, tu IMC es {imc:.2f} - Clasificación: {clasificacion}")

        with open(archivo, mode="a", newline="", encoding="latin1") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                fecha_actual,
                nombre,
                str(peso).replace('.', ','),
                str(altura).replace('.', ','),
                str(round(imc, 2)).replace('.', ','),
                clasificacion,
                actividad
            ])

    #except ValueError:
     #   print("Error: Asegúrate de introducir valores numéricos válidos para peso y altura.")

    except ValueError as e:
     print(f"Error: {e}")

def ver_registros(nombre, archivo):
    if not os.path.exists(archivo):
        print("No hay registros todavía.")
        return

    df = pd.read_csv(archivo, encoding="latin1", sep=";")
    registros = df[df["Nombre"] == nombre]

    if registros.empty:
        print("No se encontraron registros para este usuario.")
    else:
        print("\n=== Registros anteriores ===")
        print(registros.to_string(index=False))

def modificar_registro(nombre, archivo):
    if not os.path.exists(archivo):
        print("No hay registros todavía.")
        return

    try:
        df = pd.read_csv(archivo, encoding="latin1", sep=";")
        df_usuario = df[df["Nombre"] == nombre]

        if df_usuario.empty:
            print("No se encontraron registros para este usuario.")
            return

        print("\n=== Registros encontrados ===")
        print(df_usuario[["Fecha", "Peso", "Altura", "Actividad"]])

        fecha_elegida = input("\nIntroduce la fecha del registro que deseas modificar (YYYY-MM-DD): ")

        filtro = (df["Nombre"] == nombre) & (df["Fecha"] == fecha_elegida)
        if not filtro.any():
            print("No se encontró un registro con esa fecha para este usuario.")
            return

        idx = df[filtro].index[0]

        print("\nValores actuales:")
        print(df.loc[idx, ["Peso", "Altura", "Actividad"]])

        nuevo_peso = input("Introduce el nuevo peso en kilogramos (deja en blanco para no modificar): ")
        nueva_altura = input("Introduce la nueva altura en metros (deja en blanco para no modificar): ")
        nueva_actividad = input("Introduce el nuevo nivel de actividad física (bajo/medio/alto, deja en blanco para no modificar): ").lower()

        if nuevo_peso:
            df.at[idx, "Peso"] = float(nuevo_peso)
        if nueva_altura:
            df.at[idx, "Altura"] = float(nueva_altura)
        if nueva_actividad:
            df.at[idx, "Actividad"] = nueva_actividad

        #Recalcular el IMC y actualizar la clasificación

        peso = df.at[idx, "Peso"] # Obtener el peso actualizado
        altura = df.at[idx, "Altura"] # Obtener la altura actualizada
        nuevo_imc = calcular_imc(peso, altura)
        df.at[idx, "IMC"] = round(nuevo_imc, 2) # Actualizar el IMC en el CSV
        df.at[idx, "Clasificación"] = clasificar_imc(nuevo_imc) # Clasificar el nuevo IMC

        # Convertimos los valores numéricos a cadenas con coma decimal
        df["Peso"] = df["Peso"].map(lambda x: str(x).replace('.', ','))
        df["Altura"] = df["Altura"].map(lambda x: str(x).replace('.', ','))
        df["IMC"] = df["IMC"].map(lambda x: str(x).replace('.', ','))

        df.to_csv(archivo, index=False, encoding="latin1", sep=";")

        print("\n✅ Registro actualizado correctamente.")

    except Exception as e:
        print(f"Ocurrió un error al intentar modificar el registro: {e}")

# === CONFIGURACIÓN DE ARCHIVO ===

ruta_carpeta = "./data"
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
