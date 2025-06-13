# Calculadora de IMC - Librería Python

Este proyecto consiste en una **librería en Python** que permite calcular el Índice de Masa Corporal (IMC), clasificarlo, guardar registros por fecha y usuario, y analizarlos posteriormente. Está organizada correctamente como paquete instalable (`imclib`) e incluye un script interactivo y una suite de pruebas básicas.

---

## 📦 Estructura del proyecto

calculadora-imc/
├── imclib/                # Código fuente de la librería
│   ├── __init__.py
│   ├── calculo.py         # Funciones como calcular_imc(), peso_ideal(), etc.
│   └── gestion_datos.py   # Añadir, ver y modificar registros en CSV
│
├── scripts/               # Scripts ejecutables
│   └── main.py            # Interfaz por consola para probar la librería
│
├── tests/                 # Pruebas automáticas básicas
│   └── test_calculo.py
│
├── requirements.txt       # Dependencias del proyecto
├── setup.py               # Archivo para instalar la librería
└── README.md              # Este archivo

---

## ⚙️ Instalación

1. Clona o descarga este repositorio:

   git clone https://github.com/TU_USUARIO/calculadora-imc.git
   cd calculadora-imc

2. (Opcional) Crea y activa un entorno virtual:

   python -m venv .venv
   .\.venv\Scripts\activate     # En Windows

3. Instala el paquete localmente:

   pip install -e .

---

## 🚀 Uso del proyecto

### ▶️ Ejecutar la calculadora desde consola:

   python scripts/main.py

Podrás:
- Añadir un nuevo registro (nombre, peso, altura, actividad física)
- Consultar registros anteriores
- Modificar registros existentes
- Ver tu IMC, su clasificación y tu rango de peso ideal

---

## 🧪 Ejecutar tests

   python tests/test_calculo.py

---

## 📚 Funcionalidades incluidas

- calcular_imc(peso, altura)
- clasificar_imc(imc)
- peso_ideal(altura)
- mostrar_alerta_peso(peso, peso_min, peso_max)
- añadir_nuevo_registro(), ver_registros(), modificar_registro()

---

## ✅ Requisitos

Incluidos en requirements.txt:

pandas

---

## 👤 Autor

Ander Villar  
Máster en IA y Data Science  
Proyecto final del Módulo 1
