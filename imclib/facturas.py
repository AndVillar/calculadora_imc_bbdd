from datetime import datetime
from imclib.bbdd import get_connection

# === Generar un nuevo número de factura incremental ===
def generar_numero_factura():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facturas")
        total = cursor.fetchone()[0]
        return f"FAC{total + 1:03d}"  # Ej: FAC001

# === Crear una nueva factura para un cliente existente ===
def crear_factura():
    print("\n=== CREAR FACTURA ===")
    email = input("Ingrese email del usuario: ").strip()

    # 1. Buscar si existe ese email en la tabla usuarios
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellidos FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

    if not usuario:
        print("⚠️  No se encontró ningún usuario con ese email.")
        return

    cliente_id, nombre, apellidos = usuario
    print(f"Usuario encontrado: {nombre} {apellidos}")

    # 2. Solicitar información de la factura
    descripcion = input("Ingrese descripción del servicio/producto: ").strip()
    try:
        monto = float(input("Ingrese monto total: "))
        if monto <= 0:
            print("⚠️  El monto debe ser un número positivo.")
            return
    except ValueError:
        print("⚠️  El monto no es válido.")
        return

    print("Seleccione estado:")
    print("1. Pendiente")
    print("2. Pagada")
    print("3. Cancelada")
    estado_opcion = input("Estado: ").strip()
    estados = {"1": "Pendiente", "2": "Pagada", "3": "Cancelada"}
    estado = estados.get(estado_opcion)

    if not estado:
        print("⚠️  Estado no válido.")
        return

    # 3. Generar datos finales
    numero_factura = generar_numero_factura()
    fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")

    # 4. Insertar en la tabla facturas
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO facturas (numero, cliente_id, fecha_emision, descripcion, monto, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (numero_factura, cliente_id, fecha_emision, descripcion, monto, estado))
        conn.commit()

    # 5. Mostrar confirmación
    print("\n✅ Factura creada exitosamente!")
    print(f"Número de factura: {numero_factura}")
    print(f"Fecha de emisión: {fecha_emision}")
    print(f"Cliente: {nombre} {apellidos}")
    print(f"Descripción: {descripcion}")
    print(f"Monto: ${monto:.2f}")
    print(f"Estado: {estado}")

# === Mostrar facturas asociadas a un cliente por email ===
def mostrar_facturas_de_usuario():
    print("\n=== FACTURAS POR USUARIO ===")
    email = input("Ingrese email del usuario: ").strip()

    with get_connection() as conn:
        cursor = conn.cursor()
        # Buscar el cliente
        cursor.execute("SELECT id, nombre, apellidos FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            print("⚠️  No se encontró ningún usuario con ese email.")
            return

        cliente_id, nombre, apellidos = usuario
        print(f"\n--- FACTURAS DE {nombre} {apellidos} ---")

        # Buscar facturas del cliente
        cursor.execute("""
            SELECT numero, fecha_emision, descripcion, monto, estado
            FROM facturas
            WHERE cliente_id = ?
        """, (cliente_id,))
        facturas = cursor.fetchall()

        if not facturas:
            print("Este usuario no tiene facturas registradas.")
            return

        # Mostrar cada factura
        monto_total = 0
        monto_pendiente = 0

        for i, factura in enumerate(facturas, start=1):
            numero, fecha, descripcion, monto, estado = factura
            print(f"\nFactura #{i}:")
            print(f"Número: {numero}")
            print(f"Fecha: {fecha}")
            print(f"Descripción: {descripcion}")
            print(f"Monto: ${monto:.2f}")
            print(f"Estado: {estado}")

            monto_total += monto
            if estado == "Pendiente":
                monto_pendiente += monto

        print(f"\nTotal de facturas: {len(facturas)}")
        print(f"Monto total facturado: ${monto_total:.2f}")
        print(f"Monto pendiente: ${monto_pendiente:.2f}")

# === Mostrar resumen financiero por usuario ===
def mostrar_resumen_financiero():
    print("\n=== RESUMEN FINANCIERO ===")

    with get_connection() as conn:
        cursor = conn.cursor()

        # Obtener todos los usuarios
        cursor.execute("SELECT id, nombre, apellidos, email FROM usuarios")
        usuarios = cursor.fetchall()

        total_usuarios = len(usuarios)
        total_facturas = 0
        ingresos_totales = 0
        ingresos_pagados = 0
        ingresos_pendientes = 0

        for usuario in usuarios:
            cliente_id, nombre, apellidos, email = usuario

            # Obtener facturas del usuario
            cursor.execute("""
                SELECT monto, estado FROM facturas WHERE cliente_id = ?
            """, (cliente_id,))
            facturas = cursor.fetchall()

            monto_total = sum(f[0] for f in facturas)
            pagadas = sum(f[0] for f in facturas if f[1] == "Pagada")
            pendientes = sum(f[0] for f in facturas if f[1] == "Pendiente")

            print(f"\nUsuario: {nombre} {apellidos} ({email})")
            print(f"- Total facturas: {len(facturas)}")
            print(f"- Monto total: ${monto_total:.2f}")
            print(f"- Facturas pagadas: ${pagadas:.2f}")
            print(f"- Facturas pendientes: ${pendientes:.2f}")

            total_facturas += len(facturas)
            ingresos_totales += monto_total
            ingresos_pagados += pagadas
            ingresos_pendientes += pendientes

        print("\n--- RESUMEN GENERAL ---")
        print(f"Total usuarios: {total_usuarios}")
        print(f"Total facturas emitidas: {total_facturas}")
        print(f"Ingresos totales: ${ingresos_totales:.2f}")
        print(f"Ingresos recibidos: ${ingresos_pagados:.2f}")
        print(f"Ingresos pendientes: ${ingresos_pendientes:.2f}")

