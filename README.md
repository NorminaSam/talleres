# Talleres de GitHub con Copilot

## Carátula del Proyecto

- **Asignatura:** Taller de GitHub y Control de Versiones
- **Nombre del Proyecto:** Procesamiento de trámites y generación de resumen CSV
- **Autor:** Rosa Samaniego
- **Fecha:** 2026-08-11
- **Rama de trabajo:** `feature/configuracion`

## Objetivo del proyecto

Este proyecto procesa archivos CSV de trámites, valida los datos, clasifica el tiempo y genera un archivo `resumen.csv` con métricas clave. Está organizado para que cualquier persona pueda entender el flujo de datos y cómo ejecutar la tarea.

## Qué se hizo

1. Se agregó o mejoró el procesamiento de archivos CSV en `ejercicios_en_clase/procesar.py`.
2. Se incluyó validación de cédula y fecha para cada registro.
3. Se descartaron los registros inválidos o con datos incompletos.
4. Se calculó el promedio de minutos solo con registros válidos.
5. Se generó un archivo `resumen.csv` con las columnas:
   - `archivo`
   - `validos`
   - `descartados`
   - `promedio`
6. Se preparó la rama `feature/configuracion` para publicar y revisar los cambios mediante Pull Request hacia `main`.

## Archivos clave

- `ejercicios_en_clase/procesar.py`: lógica principal de lectura, validación y resumen de CSV.
- `ejercicios_en_clase/datos/`: carpeta con los archivos de datos de ejemplo (`tramites_2026-08-03.csv`, `tramites_2026-08-04.csv`, `tramites_2026-08-05.csv`).
- `ejercicios_en_clase/resumen.csv`: archivo de salida generado al ejecutar el script.
- `validacion.py`: módulo con funciones de validación usadas en el proyecto.

## Instrucciones para ejecutar la tarea

1. Abrir una terminal en el directorio del repositorio:
   ```bash
   cd /d/CURSOS/GitHubCopilot/talleres/talleres
   ```
2. Cambiar a la rama de trabajo o crearla si aún no existe:
   ```bash
   git checkout -b feature/configuracion
   ```
3. Ejecutar el script de procesamiento:
   ```bash
   python ejercicios_en_clase/procesar.py
   ```
4. Revisar el archivo generado `ejercicios_en_clase/resumen.csv`.

## Cómo publicar los cambios en GitHub

1. Agregar los cambios:
   ```bash
   git add .
   ```
2. Hacer commit:
   ```bash
   git commit -m "Agregar configuración y ajustes del procesamiento de trámites"
   ```
3. Enviar la rama al remoto:
   ```bash
   git push origin feature/configuracion
   ```
4. Crear el Pull Request hacia `main` (usando GitHub CLI o la web):
   ```bash
   gh pr create --base main --head feature/configuracion --title "Feature: configuración" --body "Se agregaron ajustes de configuración y mejoras en el procesamiento de trámites."
   ```

## Qué verificar en el Pull Request

- Que exista un PR abierto de `feature/configuracion` hacia `main`.
- Que la pestaña `Files changed` muestre los archivos modificados.
- Que la descripción del PR explique los cambios realizados y el objetivo del reajuste.
