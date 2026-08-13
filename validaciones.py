import re


def validar_cedula(cedula):
    """Valida que la cédula tenga exactamente 10 dígitos numéricos."""
    if cedula is None:
        return False

    cedula = str(cedula).strip()
    return len(cedula) == 10 and cedula.isdigit()


def validar_nombre_apellido(nombre, apellido):
    """Valida que nombre y apellido sean texto alfabético y no estén vacíos."""
    if nombre is None or apellido is None:
        return False

    nombre = str(nombre).strip()
    apellido = str(apellido).strip()

    return bool(nombre) and bool(apellido) and nombre.isalpha() and apellido.isalpha()


def validar_correo(correo):
    """Valida un formato básico de correo electrónico."""
    if correo is None:
        return False

    correo = str(correo).strip()
    if not correo or correo.count("@") != 1:
        return False

    usuario, dominio = correo.split("@")
    if not usuario or not dominio:
        return False

    if "." not in dominio:
        return False

    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(patron, correo) is not None
