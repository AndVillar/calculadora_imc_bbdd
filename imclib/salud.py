from datetime import datetime
from imclib.bbdd import get_connection

# === Calcular el IMC y clasificarlo ===
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        clasificacion = "Bajo peso"
    elif imc < 25:
        clasificacion = "Normal"
    elif imc < 30:
        clasificacion = "Sobrepeso"
    else:
        clasificacion = "Obesidad"
    return round(imc, 2), clasificacion

# === Registrar un nuevo registro IMC para un cliente existente ===
def registrar_imc():
    print("\n=== REGISTRAR NUEVO IMC ===")
    email = input("Ingrese email del usuario: ").strip()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellidos FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            print("⚠️  No se encontró ningún usuario con ese email.")
            return

        cliente_id, nombre, apellidos = usuario
        print(f"Usuario encontrado: {nombre} {apellidos}")

        try:
            peso = float(input("Ingrese peso en kg: ").replace(",", "."))
            altura = float(input("Ingrese altura en metros: ").replace(",", "."))

            if peso <= 0 or altura <= 0:
                print("⚠️  Peso y altura deben ser mayores que cero.")
                return
        except ValueError:
            print("⚠️  Error: Introduce números válidos con punto o coma decimal.")
            return

        imc, clasificacion = calcular_imc(peso, altura)
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Verificar si ya existe un IMC registrado ese día
        cursor.execute("""
            SELECT * FROM registros_imc
            WHERE cliente_id = ? AND fecha = ?
        """, (cliente_id, fecha_actual))
        if cursor.fetchone():
            print("⚠️  Ya existe un registro de IMC para este usuario hoy.")
            return

        # Insertar nuevo registro
        cursor.execute("""
            INSERT INTO registros_imc (cliente_id, fecha, peso, altura, imc, clasificacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente_id, fecha_actual, peso, altura, imc, clasificacion))
        conn.commit()

    print("\n✅ Registro de IMC guardado correctamente.")
    print(f"{nombre} {apellidos} - IMC: {imc} ({clasificacion})")

# === Mostrar historial IMC por email ===
def ver_historial_imc():
    print("\n=== HISTORIAL IMC DEL USUARIO ===")
    email = input("Ingrese email del usuario: ").strip()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellidos FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            print("⚠️  No se encontró ningún usuario con ese email.")
            return

        cliente_id, nombre, apellidos = usuario
        cursor.execute("""
            SELECT fecha, peso, altura, imc, clasificacion
            FROM registros_imc
            WHERE cliente_id = ?
            ORDER BY fecha
        """, (cliente_id,))
        registros = cursor.fetchall()

        if not registros:
            print("Este usuario no tiene registros de IMC.")
            return

        print(f"\nHistorial de {nombre} {apellidos}:")
        for r in registros:
            fecha, peso, altura, imc, clasificacion = r
            print(f"{fecha} | Peso: {peso} kg | Altura: {altura} m | IMC: {imc} ({clasificacion})")
