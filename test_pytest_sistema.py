"""Pytest suite for sistema_capacitacion.

Includes unit and simple integration tests with descriptive names and inline comments.
"""
from sistema_capacitacion import (
    SistemaCapacitacion,
    validar_cedula_ecuador,
    validar_cedula_ecuador_detalle,
)
import json


def make_valid_cedula(province: int = 1, third: int = 0) -> str:
    """Construct a valid 10-digit Ecuadorian cédula deterministically.

    We choose province (01-24 or 30) and third digit (<6), fill the middle
    digits with zeros and compute the verifier digit so the result passes
    the validator.
    """
    if not (1 <= province <= 24 or province == 30):
        raise ValueError("province must be 1-24 or 30")
    if third >= 6:
        raise ValueError("third digit must be < 6 for natural persons")
    digits = [0] * 10
    # province two digits
    digits[0] = province // 10
    digits[1] = province % 10
    digits[2] = third
    # keep digits 3..8 as zeros for determinism
    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        val = digits[i] * coef[i]
        if val >= 10:
            val -= 9
        total += val
    verifier = (10 - (total % 10)) % 10
    digits[9] = verifier
    return "".join(str(d) for d in digits)


def test_validar_cedula_generada_es_valida():
    """Validator accepts a deterministically generated valid cédula."""
    ced = make_valid_cedula(province=1, third=0)
    assert len(ced) == 10
    assert validar_cedula_ecuador(ced) is True
    ok, motivo = validar_cedula_ecuador_detalle(ced)
    assert ok and motivo == ""


def test_validar_cedula_rechaza_formato_invalido():
    """Validator rejects wrong-length or non-numeric cédulas."""
    assert validar_cedula_ecuador("123") is False
    ok, motivo = validar_cedula_ecuador_detalle("abcde12345")
    assert ok is False
    assert "10 dígitos" in motivo or "dígitos numéricos" in motivo


def test_registrar_estudiante_y_persistencia_roundtrip(tmp_path):
    """Registrar un estudiante y verificar que se persiste y se recupera."""
    sistema = SistemaCapacitacion()
    ced = make_valid_cedula(province=1, third=0)
    ok, msg = sistema.registrar_estudiante(ced, "Test", "User", "Curso X", "M")
    assert ok
    # save to temp file
    p = tmp_path / "estudiantes_tmp.json"
    ok, msg = sistema.save_to_file(str(p))
    assert ok
    # load into a new instance
    s2 = SistemaCapacitacion()
    ok, msg = s2.load_from_file(str(p))
    assert ok
    assert ced in s2.estudiantes


def test_load_omits_invalid_ids(tmp_path):
    """load_from_file should omit invalid IDs and report them in the message."""
    data = {
        "000": {"identificacion": "000", "nombres": "Bad", "apellidos": "Entry", "curso": "C", "horario": "M"},
        make_valid_cedula(province=2, third=0): {"identificacion": make_valid_cedula(province=2, third=0), "nombres": "Good", "apellidos": "Entry", "curso": "C", "horario": "T"},
    }
    p = tmp_path / "estudiantes_mixed.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    s = SistemaCapacitacion()
    ok, msg = s.load_from_file(str(p))
    assert ok
    # message must mention the omitted invalid id
    assert "omit" in msg.lower() or "omitieron" in msg.lower()
    # only the valid id should be present
    assert len(s.estudiantes) == 1


def test_registrar_asistencia_limite_por_entrada():
    """No se deben aceptar entradas de asistencia mayores a 40 horas."""
    s = SistemaCapacitacion()
    ced = make_valid_cedula(province=3, third=0)
    s.registrar_estudiante(ced, "A", "B", "C", "M")
    ok, msg = s.registrar_asistencia(ced, 1, 41)
    assert ok is False
