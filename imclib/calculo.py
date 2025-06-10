#imclib/calculo.py

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
    
def recomendar_cambio(imc):
    if imc < 18.5:
        return "Recomendación: aumentar la ingesta calórica"
    elif imc >= 25:
        return "Recomendación: aumentar la actividad física"
    else:
        return "Recomendación: mantener hábitos actuales"

def peso_ideal(altura):
    """
    Calcula un rango de peso ideal basado en un IMC entre 18.5 y 24.9.
    """
    min_peso = 18.5 * (altura ** 2)
    max_peso = 24.9 * (altura ** 2)
    return round(min_peso, 1), round(max_peso, 1)

def mostrar_alerta_peso(peso, peso_min, peso_max):
    if peso < peso_min:
        return "⚠️ Estás por debajo de tu peso ideal."
    elif peso > peso_max:
        return "⚠️ Estás por encima de tu peso ideal."
    else:
        return "✅ Estás dentro de tu rango ideal de peso."