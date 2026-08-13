# 🚀 Proyecto: Caso Integrador Final

![GitHub](https://img.shields.io/badge/GitHub-purple)
![Copilot](https://img.shields.io/badge/Copilot-blue)
![SonarQube](https://img.shields.io/badge/SonarQube-orange)

---
Aplicación web desarrollada con GitHub y Copilot.

## Integrantes
- Marcela Baldeón
- Rosa Samaniego

## Grupo
GRUPO 2

## Tecnologías
- Python 3.12
- GitHub
- SonarQube

# Sistema de Gestión de Capacitación — Carátula del Proyecto

Este repositorio contiene un sistema en Python desarrollado para la gestión de inscripción, asistencia y evaluación de estudiantes en cursos de capacitación. El presente documento actúa como carátula descriptiva del trabajo realizado: objetivos, alcance, estructura, instrucciones de uso y estado de pruebas.

## Resumen

El proyecto implementa un sistema completo que permite:

- Registrar estudiantes con validación de cédula ecuatoriana.
- Registrar asistencia por módulo (control de horas y límite por entrada).
- Registrar actividades parciales (dos parciales por módulo) y un examen final.
- Determinar habilitación para examen final según asistencia y actividades.
- Persistir y recuperar datos en formato JSON.
- Proveer una interfaz de consola mínima para interacción y pruebas automatizadas.

## Alcance y características relevantes

- Validación robusta de cédula ecuatoriana (formato y dígito verificador).
- Control de integridad al cargar datos desde archivos: entradas con cédulas inválidas se omiten y se reportan.
- Límite por entrada de asistencia: no se aceptan registros mayores a 40 horas.
- Reglas de calificación: dos actividades parciales de 30 puntos cada una y un examen final de 20 puntos.
- Persistencia en `estudiantes.json` (archivo creado junto al módulo principal cuando se guarda).

## Estructura del proyecto (relevante)

- `caso_integrador_final/` — carpeta que contiene este README y archivos del caso integrador.
- `sistema_capacitacion.py` — implementación principal del sistema (en la raíz del repositorio).
- `test_*.py` — suites de prueba automatizadas (`pytest` y `unittest`) ubicadas en la raíz del repositorio.

## Requisitos

- Python 3.8+ (se ha verificado en entornos recientes; use la versión de Python de su sistema).
- Dependencias de desarrollo: `pytest` (listada en `requirements.txt`).

## Cómo ejecutar las pruebas desde `caso_integrador_final`

Este proyecto fue configurado para permitir la ejecución de pruebas desde la carpeta `caso_integrador_final`. Para ejecutar las pruebas desde esa carpeta, abra una terminal con `CWD` en `caso_integrador_final` y ejecute:

```bash
python -m pytest -v
```

Al ejecutar desde `caso_integrador_final` el sistema usa el archivo `pytest.ini` localizado en la misma carpeta para descubrir los tests presentes en la raíz del proyecto.

## Estado de pruebas

Las pruebas unitarias e integración se han ejecutado correctamente desde `caso_integrador_final` y el conjunto completo devolvió:

- 32 pruebas aprobadas (32 passed).

## Notas de implementación y de calidad

- Se añadieron reglas para omitir archivos de extensiones del editor en análisis estático (Sonar) mediante `sonar-project.properties` para evitar falsos positivos en archivos de terceros (p. ej. `typeshed` de Pylance).
- Se centralizaron validaciones y se refactorizó código para reducir la complejidad cognitiva y duplicación de literales.

## Uso y validaciones importantes

- La entrada de cédula está validada estrictamente: la aplicación rechaza y omite datos con cédulas inválidas durante carga o registro interactivo.
- Para pruebas ad-hoc puede ejecutar el módulo principal con Python e interactuar con la interfaz de consola, si así lo desea.

## Contacto y mantenimiento

Para dudas sobre el código, mejoras o reportes de error, por favor abrir un issue en el repositorio o contactar al autor responsable del proyecto.

---

Fecha de última verificación: 2026-08-12
#Readme Caso Integrador Final
