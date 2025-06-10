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