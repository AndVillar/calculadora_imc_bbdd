import sqlite3
import os

# === Ruta absoluta al archivo de base de datos ===
# Creamos una ruta que apunta a: /data/crm.db desde donde está este archivo
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "crm.db")

# === Función para obtener la conexión a la base de datos ===
def get_connection():
    return sqlite3.connect(DB_PATH)

# === Función que inicializa las tablas si no existen ===
def inicializar_base_de_datos():
    # Abrimos conexión con la base de datos usando un context manager (se cierra sola)
    with get_connection() as conn:
        cursor = conn.cursor()

        # --- Crear tabla de USUARIOS ---
        # Contiene ID (como 'USR001'), nombre, apellidos, email único, etc.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefono TEXT,
            direccion TEXT,
            fecha_registro TEXT NOT NULL
        )
        """)

        # --- Crear tabla de FACTURAS ---
        # Asociada a un usuario por su ID. Almacena fecha, descripción, monto y estado.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            numero TEXT PRIMARY KEY,
            cliente_id TEXT NOT NULL,
            fecha_emision TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            estado TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES usuarios(id)
        )
        """)

        # --- Crear tabla de REGISTROS IMC ---
        # Registra peso, altura e IMC de cada cliente en fechas distintas.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_imc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id TEXT NOT NULL,
            fecha TEXT NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            imc REAL NOT NULL,
            clasificacion TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES usuarios(id)
        )
        """)

        # Guardar los cambios (commit)
        conn.commit()
