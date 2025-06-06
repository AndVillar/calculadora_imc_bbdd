# tests/test_calculo.py

from imclib.calculo import calcular_imc, clasificar_imc

def test_imc():
    peso = 70
    altura = 1.75
    imc = calcular_imc(peso, altura)
    assert round(imc, 2) == 22.86
    assert clasificar_imc(imc) == "Normal"

if __name__ == "__main__":
    test_imc()
    print("✅ Test pasado correctamente.")
