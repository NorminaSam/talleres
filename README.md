# Talleres de GitHub con Copilot

## Carátula del Proyecto

- **Asignatura:** Taller de GitHub y Control de Versiones
- **Nombre del Proyecto:** Procesamiento de trámites y validaciones de datos
- **Autor:** Rosa Samaniego
- **Fecha:** 2026-08-11
- **Rama de trabajo:** `feature/caso-integrador-final`

## Objetivo del proyecto

Este repositorio combina dos líneas de trabajo: la validación de datos básicos y el procesamiento de trámites con resumen CSV. El objetivo es demostrar el uso de GitHub, control de versiones y automatización de pruebas en un proyecto práctico.

## Qué incluye

1. Validación de cédula, nombre/apellido y correo electrónico para formularios simples.
2. Procesamiento de archivos CSV de trámites con validación y clasificación del tiempo.
3. Generación de `resumen.csv` con métricas clave.
4. Estructura lista para revisión, merge y publicación en GitHub.

## Archivos clave

- `validaciones.py`: funciones para validar cédula, nombre/apellido y correo.
- `validacion.py`: validación básica adicional para cédula y correo.
- `ejercicios_en_clase/procesar.py`: lectura, validación y resumen de archivos CSV.
- `ejercicios_en_clase/datos/`: archivos de ejemplo para pruebas.
- `ejercicios_en_clase/resumen.csv`: salida generada por el script.

## Uso rápido

```python
from validaciones import validar_cedula, validar_nombre_apellido, validar_correo

print(validar_cedula("0991234567"))
print(validar_nombre_apellido("Ana", "Pérez"))
print(validar_correo("ana@ejemplo.com"))
```

## Ejecutar la tarea

```bash
python ejercicios_en_clase/procesar.py
```

## Publicación en GitHub

```bash
git add .
git commit -m "Sincronizar rama con main"
git push origin HEAD:caso_integrador_final
```

## Estado

Proyecto consolidado, listo para revisión con `main` y publicación de la rama final.
