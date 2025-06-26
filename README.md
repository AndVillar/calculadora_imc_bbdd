CRM + CALCULADORA IMC - PROYECTO FINAL MÓDULO 1

Este proyecto combina un sistema básico de gestión de relaciones con clientes (CRM) con una herramienta de seguimiento de salud mediante cálculo de IMC (Índice de Masa Corporal).

Está desarrollado como una librería Python estructurada en módulos, con interfaz por consola, base de datos SQLite, y funcionalidades útiles tanto para usuarios como para administración.

---------------------------------------------------------
FUNCIONALIDADES PRINCIPALES

- Registro de usuarios
- Gestión de facturas asociadas a cada usuario
- Cálculo de IMC con clasificación nutricional
- Historial de salud por usuario
- Resumen financiero por usuario y global
- Visualización por consola en formato de tabla (con tabulate)
- Modo administrador oculto con opciones extendidas

---------------------------------------------------------
ESTRUCTURA DEL PROYECTO

Proyecto_IMC_BBDD/
│
├── imclib/                  → Librería principal del sistema
│   ├── __init__.py
│   ├── bbdd.py              → Inicialización y conexión a SQLite
│   ├── usuarios.py          → Registro, búsqueda y visualización de usuarios
│   ├── facturas.py          → Crear, consultar y resumir facturas
│   ├── salud.py             → Registrar y consultar IMC
│   └── gestion_datos.py     → Módulo antiguo para IMC vía CSV
│
├── scripts/
│   └── seed_db.py           → Script para llenar la base de datos con datos simulados
│
├── data/
│   └── crm.db               → Base de datos SQLite con toda la información
│
├── main.py                  → Script principal con menú interactivo
├── setup.py                 → Instalador del paquete como librería Python
├── README.md                → Este archivo
└── requirements.txt         → (opcional) listado de dependencias

---------------------------------------------------------
INSTRUCCIONES DE INSTALACIÓN Y USO

1. Clona el repositorio:

   git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
   cd TU-REPOSITORIO

2. Crea un entorno virtual (opcional pero recomendado):

   python -m venv .venv
   .venv\Scripts\activate     (en Windows)

3. Instala el paquete en modo editable:

   pip install -e .

4. Ejecuta el programa principal:

   python main.py

---------------------------------------------------------
FUNCIONES DISPONIBLES DESDE EL MENÚ

1. Registrar nuevo usuario
2. Ver usuario por email o nombre
3. Crear factura para usuario
4. Mostrar facturas de un usuario
5. Resumen financiero por usuario
6. Módulo de Salud (registrar y consultar IMC)
7. Salir

MENÚ ADMIN (oculto): si se introduce la opción "010"
- Ver todos los usuarios registrados (en formato tabla)
- Otras funciones futuras de administración

---------------------------------------------------------
AUTOR

Ander Villar  
Máster en IA y Data Science  

---------------------------------------------------------
NOTAS

- Proyecto desarrollado para ser ejecutado desde consola
- Compatible con expansión futura (ej. API, interfaz gráfica, exportación Power BI)
- Puede integrarse con datos reales si se desea
