import re

def validar_cedula(cedula):
    return isinstance(cedula, str) and len(cedula) == 10 and cedula.isdigit()

def validar_correo(correo):
    if not isinstance(correo, str):
        return False

    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(patron, correo) is not None