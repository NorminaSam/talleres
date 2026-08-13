# Función que valide una cédula tenga 10 dígitos numéricos
def validar_cedula(cedula: str) -> bool:
    if cedula is None or len(cedula) != 10 or not cedula.isdigit():
        return False
    return True


# Función que valide un correo electrónico
def validar_correo(correo: str) -> bool:    
    if correo is None or len(correo) == 0 or '@' not in correo:
        return False
    return True


