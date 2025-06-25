import random
from datetime import datetime, timedelta
from imclib.bbdd import get_connection
from imclib.salud import calcular_imc

# === Datos simulados ===
nombres = ["Juan", "Ander", "Carlos", "Laura", "Pedro", "Lucía", "Ander", "Ana", "Luis", "Sofía"]
apellidos = ["Pérez", "Villar", "Rodríguez", "López", "Martínez", "Sánchez", "Romero", "Díaz", "Fernández", "Villar"]
dominios = ["email.com", "correo.com", "test.org"]

# === Semilla para reproducibilidad ===
random.seed(42)


with get_connection() as conn:
    cursor = conn.cursor()
    
    # Borra los datos existentes
    cursor.execute("DELETE FROM registros_imc")
    cursor.execute("DELETE FROM facturas")
    cursor.execute("DELETE FROM usuarios")
    # ...resto del código...

    for i in range(10):
        nombre = nombres[i]
        apellido = apellidos[i]
        email = f"{nombre.lower()}.{apellido.lower()}@{random.choice(dominios)}"
        telefono = f"555-{random.randint(1000,9999)}"
        direccion = f"Calle {random.randint(1, 50)}"
        fecha_registro = (datetime.today() - timedelta(days=random.randint(1, 300))).strftime("%d/%m/%Y")
        usuario_id = f"USR{i+1:03d}"

        # Insertar usuario
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, apellidos, email, telefono, direccion, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (usuario_id, nombre, apellido, email, telefono, direccion, fecha_registro))

        # Crear 2-3 facturas
        for j in range(random.randint(2, 3)):
            factura_id = f"FAC{(i*3)+j+1:03d}"
            fecha = (datetime.today() - timedelta(days=random.randint(1, 60))).strftime("%d/%m/%Y %H:%M")
            descripcion = random.choice(["Consulta nutricional", "Entrenamiento", "Revisión médica"])
            monto = round(random.uniform(100, 900), 2)
            estado = random.choice(["Pendiente", "Pagada", "Cancelada"])
            cursor.execute("""
                INSERT INTO facturas (numero, cliente_id, fecha_emision, descripcion, monto, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (factura_id, usuario_id, fecha, descripcion, monto, estado))

        # Crear 3-5 registros IMC
        fecha_inicio = datetime.today() - timedelta(days=90)
        for k in range(random.randint(3, 5)):
            fecha = (fecha_inicio + timedelta(days=7*k)).strftime("%Y-%m-%d")
            peso = round(random.uniform(55, 100), 1)
            altura = round(random.uniform(1.55, 1.90), 2)
            imc, clasificacion = calcular_imc(peso, altura)

            cursor.execute("""
                INSERT INTO registros_imc (cliente_id, fecha, peso, altura, imc, clasificacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (usuario_id, fecha, peso, altura, imc, clasificacion))

    conn.commit()

print("✅ Base de datos rellenada con usuarios, facturas e IMC simulados.")
