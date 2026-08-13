import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parent / "__pycache__" / "Ejercicios en clase" / "tramites.py"
SPEC = importlib.util.spec_from_file_location("tramites_module", MODULE_PATH)
tramites = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tramites)

validar_cedula = tramites.validar_cedula
validar_fecha = tramites.validar_fecha
clasificar_tiempo = tramites.clasificar_tiempo
calcular_promedio = tramites.calcular_promedio
resumen_diario = tramites.resumen_diario


# ---------------------------------------------------------------------------
# Módulo principal: pruebas de tramites.py
# ---------------------------------------------------------------------------


def test_validar_cedula_normal():
    assert validar_cedula("0991234567") is True


def test_validar_cedula_limite():
    assert validar_cedula("0000000000") is True


def test_validar_cedula_error():
    assert validar_cedula(None) is False
    assert validar_cedula("123456789") is False
    assert validar_cedula("123456789A") is False
    assert validar_cedula("") is False


def test_validar_fecha_normal():
    assert validar_fecha("15/03/2024") is True


def test_validar_fecha_limite():
    assert validar_fecha("29/02/2024") is True
    assert validar_fecha("31/12/2024") is True


def test_validar_fecha_error():
    assert validar_fecha(None) is False
    assert validar_fecha("31/02/2024") is False
    assert validar_fecha("99/13/2024") is False
    assert validar_fecha("abc") is False


def test_clasificar_tiempo_normal():
    assert clasificar_tiempo(5) == "Ágil"
    assert clasificar_tiempo(20) == "Normal"
    assert clasificar_tiempo(45) == "Demorada"


def test_clasificar_tiempo_limite():
    assert clasificar_tiempo(0) == "Ágil"
    assert clasificar_tiempo(10) == "Ágil"
    assert clasificar_tiempo(11) == "Normal"
    assert clasificar_tiempo(30) == "Normal"
    assert clasificar_tiempo(31) == "Demorada"


def test_clasificar_tiempo_error():
    with pytest.raises(ValueError):
        clasificar_tiempo(-1)


def test_calcular_promedio_normal():
    assert calcular_promedio([10, 20, 30]) == 20.0


def test_calcular_promedio_limite():
    assert calcular_promedio([]) == 0.0
    assert calcular_promedio([0]) == 0.0


def test_calcular_promedio_error():
    with pytest.raises(TypeError):
        calcular_promedio(["a", 5])


def test_resumen_diario_normal():
    registros = [
        {"cedula": "0991234567", "fecha": "15/03/2024", "minutos": 5},
        {"cedula": "0991234568", "fecha": "16/03/2024", "minutos": 25},
    ]

    resultado = resumen_diario(registros)

    assert resultado["total"] == 2
    assert resultado["descartados"] == 0
    assert resultado["promedio"] == 15.0
    assert resultado["categorias"]["Ágil"] == 1
    assert resultado["categorias"]["Normal"] == 1


def test_resumen_diario_limite():
    resultado = resumen_diario([])
    assert resultado == {
        "total": 0,
        "descartados": 0,
        "promedio": 0.0,
        "categorias": {"Ágil": 0, "Normal": 0, "Demorada": 0},
    }


def test_resumen_diario_error():
    registros = [
        {"cedula": "123", "fecha": "31/02/2024", "minutos": -1},
        {"cedula": "0991234567", "fecha": "15/03/2024", "minutos": 5},
    ]

    resultado = resumen_diario(registros)

    assert resultado["total"] == 1
    assert resultado["descartados"] == 1
    assert resultado["promedio"] == 5.0
    assert resultado["categorias"]["Ágil"] == 1


# ---------------------------------------------------------------------------
# Auxiliares adicionales para validación de edad
# ---------------------------------------------------------------------------


def validar_edad(edad):
    if not isinstance(edad, int):
        raise TypeError("La edad debe ser un número entero")
    if edad < 0:
        raise ValueError("La edad debe ser un número positivo")
    return True


def validar_edad_rango(edad):
    if not isinstance(edad, int):
        raise TypeError("La edad debe ser un número entero")
    if edad < 18 or edad > 65:
        raise ValueError("La edad debe estar entre 18 y 65 años")
    return True


@pytest.mark.parametrize("cedula,esperado", [
    ("0991234567", True),
    ("0991234568", True),
    ("123456789", False),
    ("123456789A", False),
    ("", False),
])
def test_validar_cedula_parametrizado(cedula, esperado: bool):
    assert validar_cedula(cedula) == esperado


@pytest.mark.parametrize("edad,es_valida", [
    (16, False),
    (18, True),
    (65, True),
    (66, False),
])
def test_validar_edad_rango_parametrizado(edad: int, es_valida: bool):
    if es_valida:
        assert validar_edad_rango(edad) is True
    else:
        with pytest.raises(ValueError):
            validar_edad_rango(edad)