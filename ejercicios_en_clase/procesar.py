import csv
from pathlib import Path

from tramites import validar_cedula, validar_fecha, clasificar_tiempo


def procesar_csv(ruta_csv: Path) -> dict:
    """Procesa un CSV de trámites y devuelve las métricas del archivo."""
    total_validos = 0
    descartados = 0
    suma_minutos = 0

    with ruta_csv.open(newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            cedula = fila.get('cedula')
            fecha = fila.get('fecha')
            minutos = fila.get('minutos')

            if not validar_cedula(str(cedula)) or not validar_fecha(str(fecha)):
                descartados += 1
                continue

            try:
                minutos_int = int(minutos)
            except (TypeError, ValueError):
                descartados += 1
                continue

            try:
                clasificar_tiempo(minutos_int)
            except ValueError:
                descartados += 1
                continue

            total_validos += 1
            suma_minutos += minutos_int

    promedio = round(suma_minutos / total_validos, 2) if total_validos else 0.0
    return {
        'archivo': ruta_csv.name,
        'validos': total_validos,
        'descartados': descartados,
        'promedio': promedio,
    }


def generar_resumen(datos_dir: Path, salida: Path) -> None:
    """Lee todos los CSV en el directorio datos_dir y escribe resumen.csv."""
    filas_salida = []

    for ruta_csv in sorted(datos_dir.glob('*.csv')):
        if ruta_csv.is_file():
            resumen = procesar_csv(ruta_csv)
            filas_salida.append(resumen)

    with salida.open('w', newline='', encoding='utf-8') as archivo:
        campos = ['archivo', 'validos', 'descartados', 'promedio']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas_salida)


if __name__ == '__main__':
    carpeta_datos = Path(__file__).resolve().parent / 'datos'
    ruta_salida = Path(__file__).resolve().parent / 'resumen.csv'
    generar_resumen(carpeta_datos, ruta_salida)
    print(f'Resumen generado en: {ruta_salida}')

