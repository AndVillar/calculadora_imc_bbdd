import re
from datetime import datetime
from tabulate import tabulate
from imclib.bbdd import get_connection

# === Validar que el email tenga un formato válido ===
def email_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email)

# === Obtener el siguiente ID disponible en formato USR001, USR002... ===
def generar_nuevo_id():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        nuevo_id = f"USR{total + 1:03d}"  # rellena con ceros (ej: USR007)
        return nuevo_id

# === Registrar un nuevo usuario ===
def registrar_usuario():
    print("\n=== REGISTRO DE NUEVO USUARIO ===")

    # --- Solicitar los datos necesarios ---
    nombre = input("Ingrese nombre: ").strip()
    apellidos = input("Ingrese apellidos: ").strip()
    email = input("Ingrese email: ").strip()
    telefono = input("Ingrese teléfono (opcional): ").strip()
    direccion = input("Ingrese dirección (opcional): ").strip()
    fecha_registro = datetime.today().strftime('%d/%m/%Y')

    # --- Validar campos obligatorios ---
    if not nombre or not apellidos or not email:
        print("⚠️  Error: nombre, apellidos y email son obligatorios.")
        return

    # --- Validar formato de email ---
    if not email_valido(email):
        print("⚠️  Error: el email no tiene un formato válido.")
        return

    # --- Verificar si el email ya está en uso ---
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            print("⚠️  Error: ya existe un usuario con ese email.")
            return

        # --- Generar ID y guardar el usuario ---
        nuevo_id = generar_nuevo_id()
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, apellidos, email, telefono, direccion, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nuevo_id, nombre, apellidos, email, telefono or None, direccion or None, fecha_registro))
        conn.commit()

    # --- Mostrar confirmación ---
    print("\n✅ Usuario registrado exitosamente!")
    print(f"ID asignado: {nuevo_id}")
    print(f"Fecha de registro: {fecha_registro}")


# === Buscar usuario por email o nombre ===
def ver_usuario():
    print("\n=== BUSCAR USUARIO ===")
    print("1. Buscar por email")
    print("2. Buscar por nombre")
    metodo = input("Seleccione método de búsqueda: ").strip()

    if metodo == "1":
        email = input("Ingrese email: ").strip()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            usuario = cursor.fetchone()

        if usuario:
            print("\n--- USUARIO ENCONTRADO ---")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]} {usuario[2]}")
            print(f"Email: {usuario[3]}")
            print(f"Teléfono: {usuario[4] or 'No especificado'}")
            print(f"Dirección: {usuario[5] or 'No especificada'}")
            print(f"Fecha de registro: {usuario[6]}")
        else:
            print("⚠️  No se encontró un usuario con ese email.")

    elif metodo == "2":
        nombre = input("Ingrese nombre: ").strip()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE nombre LIKE ?", (f"%{nombre}%",))
            resultados = cursor.fetchall()

        if resultados:
            for i, usuario in enumerate(resultados, start=1):
                print(f"\n--- USUARIO #{i} ---")
                print(f"ID: {usuario[0]}")
                print(f"Nombre: {usuario[1]} {usuario[2]}")
                print(f"Email: {usuario[3]}")
                print(f"Teléfono: {usuario[4] or 'No especificado'}")
                print(f"Dirección: {usuario[5] or 'No especificada'}")
                print(f"Fecha de registro: {usuario[6]}")
        else:
            print("⚠️  No se encontraron usuarios con ese nombre.")

    else:
        print("❌ Opción no válida.")

# === Mostrar todos los usuarios registrados ===
def ver_todos_los_usuarios():
    print("\n=== LISTA DE USUARIOS REGISTRADOS ===")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre || ' ' || apellidos AS nombre_completo, email, 
                   COALESCE(telefono, 'No especificado') AS telefono,
                   fecha_registro
            FROM usuarios
            ORDER BY id
        """)
        usuarios = cursor.fetchall()

        if not usuarios:
            print("No hay usuarios registrados.")
            return

        headers = ["ID", "Nombre", "Email", "Teléfono", "Fecha Registro"]
        print(tabulate(usuarios, headers=headers, tablefmt="grid"))
        print(f"\nTotal de usuarios: {len(usuarios)}")