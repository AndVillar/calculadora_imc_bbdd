# imclib/gestion_datos.py

import os
import csv
import pandas as pd
from datetime import datetime
from .calculo import calcular_imc, clasificar_imc
from .calculo import calcular_imc, clasificar_imc, peso_ideal

def crear_archivo_si_no_existe(archivo, cabecera):
    if not os.path.exists(archivo):
        with open(archivo, mode="w", newline="", encoding="latin1") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(cabecera)


def añadir_nuevo_registro(nombre, archivo):
    try:
        peso = float(input("Introduce tu peso en kilogramos (ej: 70): ").strip().replace(',', '.'))
        altura = float(input("Introduce tu altura en metros (ej: 1.75): ").strip().replace(',', '.'))
        actividad = input("¿Cuál es tu nivel de actividad física? (bajo/medio/alto): ").lower()
        fecha_actual = datetime.today().strftime('%Y-%m-%d')

        if os.path.exists(archivo):
            df = pd.read_csv(archivo, encoding="latin1", sep=";")
            existe = ((df["Nombre"] == nombre) & (df["Fecha"] == fecha_actual)).any()
            if existe:
                print(f"\nYa existe un registro para {nombre} en la fecha {fecha_actual}.")
                return

        imc = calcular_imc(peso, altura)
        clasificacion = clasificar_imc(imc)

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

        print(f"\n{nombre}, tu IMC es {imc:.2f} - Clasificación: {clasificacion}")
        
        peso_min, peso_max = peso_ideal(altura)
        print(f"Tu peso ideal está entre {peso_min} kg y {peso_max} kg.")

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

        nuevo_peso = input("Introduce el nuevo peso (deja en blanco para no modificar): ").strip().replace(',', '.')
        nueva_altura = input("Introduce la nueva altura (deja en blanco para no modificar): ").strip().replace(',', '.')
        nueva_actividad = input("Introduce el nuevo nivel de actividad física (deja en blanco para no modificar): ").lower()

        if nuevo_peso:
            df.at[idx, "Peso"] = float(nuevo_peso)
        if nueva_altura:
            df.at[idx, "Altura"] = float(nueva_altura)
        if nueva_actividad:
            df.at[idx, "Actividad"] = nueva_actividad

        # Recalcular IMC y clasificación
        peso = df.at[idx, "Peso"]
        altura = df.at[idx, "Altura"]
        nuevo_imc = calcular_imc(peso, altura)
        df.at[idx, "IMC"] = round(nuevo_imc, 2)
        df.at[idx, "Clasificación"] = clasificar_imc(nuevo_imc)

        # Reconvertir a coma decimal
        df["Peso"] = df["Peso"].map(lambda x: str(x).replace('.', ','))
        df["Altura"] = df["Altura"].map(lambda x: str(x).replace('.', ','))
        df["IMC"] = df["IMC"].map(lambda x: str(x).replace('.', ','))

        df.to_csv(archivo, index=False, encoding="latin1", sep=";")

        print("\n✅ Registro actualizado correctamente.")

    except Exception as e:
        print(f"Ocurrió un error al intentar modificar el registro: {e}")
