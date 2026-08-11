# Módulo de gestión de trámites de atención ciudadana.
# Usa solo la librería estándar de Python.
# Valida que una cédula tenga exactamente 10 dígitos numéricos.
# Recibe str y devuelve bool.
# Devuelve False si es None, si está vacía o si contiene letras.
def validar_cedula(cedula: str) -> bool:
    if cedula is None or len(cedula) != 10 or not cedula.isdigit():
        return False
    return True

# Valida una fecha en formato dd/mm/aaaa que exista realmente.
# Rechaza 31/02/2026 y los meses fuera del rango 1 a 12.
def validar_fecha(texto: str) -> bool:  
    if len(texto) != 10 or texto[2] != '/' or texto[5] != '/':
        return False
    try:
        dia = int(texto[0:2])
        mes = int(texto[3:5])
        anio = int(texto[6:10])
    except ValueError:
        return False
    if mes < 1 or mes > 12:
        return False
    if dia < 1:
        return False
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        return dia <= 31
    elif mes in [4, 6, 9, 11]:
        return dia <= 30
    else:  # febrero
        if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):
            return dia <= 29
        else:
            return dia <= 28  

# Clasifica el tiempo de atención de un trámite.
# Ágil: hasta 10 minutos, inclusive. Normal: de 11 a 30.
# Demorada: más de 30. Lanza ValueError si es negativo.
# Ejemplos: 10 -> "Ágil" 11 -> "Normal" 31 -> "Demorada"
def clasificar_tiempo(minutos: int) -> str:
    if minutos < 0:
        raise ValueError("El tiempo no puede ser negativo")
    if minutos <= 10:
        return "Ágil"
    if minutos <= 30:
        return "Normal"
    return "Demorada"

# Calcula el promedio de minutos, redondeado a dos decimales.
# Para una lista vacía devuelve 0.0, sin lanzar excepción.
def calcular_promedio(tiempos: list) -> float:
    if not tiempos:
        return 0.0
    return round(sum(tiempos) / len(tiempos), 2)

# Consolida una lista de registros con cedula, fecha y minutos.
# Descarta los registros inválidos sin detener el proceso.
# Devuelve un diccionario con total, descartados, promedio
# y el conteo por categoría.
def resumen_diario(registros: list) -> dict:
    total = 0
    descartados = 0
    suma = 0
    conteo = {"Ágil": 0, "Normal": 0, "Demorada": 0}

    for registro in registros:
        if isinstance(registro, dict):
            cedula = registro.get("cedula")
            fecha = registro.get("fecha")
            minutos = registro.get("minutos")
        elif isinstance(registro, (list, tuple)) and len(registro) == 3:
            cedula, fecha, minutos = registro
        else:
            descartados += 1
            continue

        if not validar_cedula(str(cedula)) or not validar_fecha(str(fecha)):
            descartados += 1
            continue

        try:
            minutos_int = int(minutos)
            categoria = clasificar_tiempo(minutos_int)
        except (ValueError, TypeError):
            descartados += 1
            continue

        total += 1
        suma += minutos_int
        conteo[categoria] += 1

    promedio = round(suma / total, 2) if total else 0.0
    return {"total": total, "descartados": descartados, "promedio": promedio, "conteo": conteo}


