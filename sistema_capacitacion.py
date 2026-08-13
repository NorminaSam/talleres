"""
Sistema de Registro y Control Académico para Curso de Capacitación

Este módulo implementa clases y un menú interactivo en consola para:
- Registrar estudiantes (sin duplicados por cédula)
- Registrar asistencia por módulo
- Registrar actividades parciales (máx 30 pts)
- Validar habilitación para examen final
- Registrar examen final (máx 20 pts)
- Mostrar reporte final

Incluye datos de prueba demostrando tres casos solicitados.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, List
import json
import os
import logging

logger = logging.getLogger(__name__)


HORARIOS_VALIDOS = {"M": "08:00-10:00", "T": "16:00-18:00"}
HORARIO_NOMBRE = {"M": "Mañana (08h00-10h00)", "T": "Tarde (16h00-18h00)"}
DATA_FILE = os.path.join(os.path.dirname(__file__), "estudiantes.json")

# Mensajes reutilizables (evitan duplicación de literales)
MSG_ESTUDIANTE_NO_ENCONTRADO = "Estudiante no encontrado."
MSG_ESTUDIANTE_REGISTRADO = "Estudiante registrado correctamente."
MSG_CALIFICACION_INVALIDA = "Calificación inválida."
MSG_VALORES_INVALIDOS_MODULO_HORAS = "Valores inválidos. Módulo debe ser 1 o 2; horas número."
MSG_OPCION_INVALIDA = "Opción inválida. Intente de nuevo."
MSG_GUARDADO_ERROR = "Error al guardar datos: {0}"

# Literales reutilizables para reducir duplicación (S1192)
DEFAULT_CURSO_PYTHON_BASICO = "Python Básico"
PROMPT_CEDULA = "Cédula/ID: "
PROMPT_NOMBRES = "Nombres: "
PROMPT_APELLIDOS = "Apellidos: "
PROMPT_CURSO = "Curso: "
PROMPT_HORARIOS = "Horarios válidos: M (mañana), T (tarde)"
PROMPT_SELECC_HORARIO = "Seleccione horario (M/T): "
PROMPT_MODULO = "Módulo (1/2): "
PROMPT_HORAS = "Horas a registrar: "
PROMPT_PRESENTO = "¿Presentó la actividad? (S/N): "
PROMPT_CAL_030 = "Calificación (0-30): "
PROMPT_CAL_EXAM = "Calificación examen final (0-20): "
PROMPT_SELECT_OPTION = "Seleccione una opción: "
MSG_NO_ESTUDIANTES = "No hay estudiantes registrados."
MSG_MODULO_INVALIDO = "Módulo inválido."


def validar_cedula_ecuador(cedula: str) -> bool:
    """Valida cédula ecuatoriana de 10 dígitos.

    Algoritmo para personas naturales:
    - Debe tener 10 dígitos numéricos
    - Los dos primeros entre 01 y 24 (provincia) o 30 para extranjeros
    - El tercer dígito debe ser < 6
    - Dígito verificador: aplicar coeficientes (2,1,2,1,2,1,2,1,2) y reglas de suma
    """
    c = cedula.strip()
    if not c.isdigit() or len(c) != 10:
        return False
    province = int(c[0:2])
    if not (1 <= province <= 24 or province == 30):
        return False
    third = int(c[2])
    if third >= 6:
        return False
    digits = [int(x) for x in c]
    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        val = digits[i] * coef[i]
        if val >= 10:
            val = val - 9
        total += val
    verifier = (10 - (total % 10)) % 10
    return verifier == digits[9]


def validar_cedula_ecuador_detalle(cedula: str) -> Tuple[bool, str]:
    """Valida cédula y devuelve (valida, motivo). Motivo vacío si es válida."""
    c = cedula.strip()
    if not c.isdigit() or len(c) != 10:
        return False, "Debe contener 10 dígitos numéricos."
    province = int(c[0:2])
    if not (1 <= province <= 24 or province == 30):
        return False, "Código de provincia inválido."
    third = int(c[2])
    if third >= 6:
        return False, "Tercer dígito inválido para persona natural."
    digits = [int(x) for x in c]
    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i in range(9):
        val = digits[i] * coef[i]
        if val >= 10:
            val = val - 9
        total += val
    verifier = (10 - (total % 10)) % 10
    if verifier != digits[9]:
        return False, "Dígito verificador inválido."
    return True, ""


@dataclass
class Modulo:
    numero: int
    horas_programadas: int = 20
    horas_asistidas: float = 0.0

    def registrar_asistencia(self, horas: float) -> Tuple[bool, str]:
        if horas < 0:
            return False, "Las horas a registrar deben ser positivas."
        nuevo_total = self.horas_asistidas + horas
        if nuevo_total > self.horas_programadas:
            return False, f"No se puede exceder {self.horas_programadas} horas por módulo. (Intentó: {nuevo_total})"
        self.horas_asistidas = round(nuevo_total, 2)
        return True, "Asistencia registrada correctamente."

    @property
    def horas_faltantes(self) -> float:
        return max(0.0, self.horas_programadas - self.horas_asistidas)

    @property
    def porcentaje_asistencia(self) -> float:
        if self.horas_programadas == 0:
            return 0.0
        return round((self.horas_asistidas / self.horas_programadas) * 100, 2)

    def cumple_asistencia_minima(self, minima: int = 15) -> bool:
        return self.horas_asistidas >= minima

    def to_dict(self) -> Dict:
        return {
            "numero": self.numero,
            "horas_programadas": self.horas_programadas,
            "horas_asistidas": self.horas_asistidas,
        }

    @staticmethod
    def from_dict(d: Dict) -> "Modulo":
        return Modulo(d.get("numero", 0), d.get("horas_programadas", 20), d.get("horas_asistidas", 0.0))


@dataclass
class ActividadParcial:
    presentada: bool = False
    calificacion: Optional[float] = None  # 0-30

    def to_dict(self) -> Dict:
        return {"presentada": self.presentada, "calificacion": self.calificacion}

    @staticmethod
    def from_dict(d: Dict) -> "ActividadParcial":
        return ActividadParcial(presentada=d.get("presentada", False), calificacion=d.get("calificacion"))


@dataclass
class Estudiante:
    identificacion: str
    nombres: str
    apellidos: str
    curso: str
    horario: str  # 'M' o 'T'
    mod1: Modulo = field(default_factory=lambda: Modulo(1))
    mod2: Modulo = field(default_factory=lambda: Modulo(2))
    actividad1: ActividadParcial = field(default_factory=ActividadParcial)
    actividad2: ActividadParcial = field(default_factory=ActividadParcial)
    examen_final: Optional[float] = None  # 0-20

    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"

    def to_dict(self) -> Dict:
        return {
            "identificacion": self.identificacion,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "curso": self.curso,
            "horario": self.horario,
            "mod1": self.mod1.to_dict(),
            "mod2": self.mod2.to_dict(),
            "actividad1": self.actividad1.to_dict(),
            "actividad2": self.actividad2.to_dict(),
            "examen_final": self.examen_final,
        }

    @staticmethod
    def from_dict(d: Dict) -> "Estudiante":
        est = Estudiante(
            d["identificacion"],
            d.get("nombres", ""),
            d.get("apellidos", ""),
            d.get("curso", ""),
            d.get("horario", "M"),
        )
        est.mod1 = Modulo.from_dict(d.get("mod1", {}))
        est.mod2 = Modulo.from_dict(d.get("mod2", {}))
        est.actividad1 = ActividadParcial.from_dict(d.get("actividad1", {}))
        est.actividad2 = ActividadParcial.from_dict(d.get("actividad2", {}))
        est.examen_final = d.get("examen_final")
        return est


class SistemaCapacitacion:
    def __init__(self):
        self.estudiantes: Dict[str, Estudiante] = {}

    # Persistencia: guardar y cargar desde JSON
    def save_to_file(self, path: str) -> Tuple[bool, str]:
        try:
            data = {k: v.to_dict() for k, v in self.estudiantes.items()}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, f"Datos guardados en {path}"
        except (IOError, OSError) as e:
            return False, f"Error al guardar datos: {e}"

    def load_from_file(self, path: str) -> Tuple[bool, str]:
        if not os.path.exists(path):
            return False, "Archivo no existe."
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            estudiantes: Dict[str, Estudiante] = {}
            invalid_ids: List[str] = []
            for k, v in data.items():
                # validar que la clave sea una cédula válida
                valid, motivo = validar_cedula_ecuador_detalle(str(k))
                if not valid:
                    invalid_ids.append(f"{k} ({motivo})")
                    continue
                est = Estudiante.from_dict(v)
                estudiantes[k] = est
            self.estudiantes = estudiantes
            if invalid_ids:
                return True, f"Datos cargados desde {path}. Se omitieron identificaciones inválidas: {', '.join(invalid_ids)}"
            return True, f"Datos cargados desde {path}"
        except (IOError, OSError, json.JSONDecodeError) as e:
            return False, f"Error al cargar datos: {e}"

    # 1. Registro de estudiantes
    def registrar_estudiante(self, identificacion: str, nombres: str, apellidos: str, curso: str, horario: str) -> Tuple[bool, str]:
        identificacion = identificacion.strip()
        if not identificacion:
            return False, "La identificación no puede estar vacía."
        if identificacion in self.estudiantes:
            return False, "Ya existe un estudiante con esa identificación."
        horario = horario.upper()
        if horario not in HORARIOS_VALIDOS:
            return False, f"Horario inválido. Use 'M' para mañana o 'T' para tarde. Horarios válidos: {', '.join(HORARIOS_VALIDOS.keys())}"
        estudiante = Estudiante(identificacion, nombres.strip(), apellidos.strip(), curso.strip(), horario)
        self.estudiantes[identificacion] = estudiante
        return True, "Estudiante registrado correctamente."

    def consultar_estudiantes(self) -> List[Estudiante]:
        return list(self.estudiantes.values())

    def obtener_estudiante(self, identificacion: str) -> Optional[Estudiante]:
        return self.estudiantes.get(identificacion.strip())

    # Helpers para validación (reducen complejidad cognitiva de la función principal)
    def _check_asistencias(self, est: Estudiante) -> List[str]:
        motivos: List[str] = []
        if not est.mod1.cumple_asistencia_minima():
            motivos.append("El estudiante no cumple con la asistencia mínima requerida para el Módulo 1.")
        if not est.mod2.cumple_asistencia_minima():
            motivos.append("El estudiante no cumple con la asistencia mínima requerida para el Módulo 2.")
        return motivos

    def _check_actividades_presentadas(self, est: Estudiante) -> List[str]:
        motivos: List[str] = []
        if not est.actividad1.presentada or est.actividad1.calificacion is None:
            motivos.append("El estudiante no ha presentado y calificado la actividad parcial del Módulo 1.")
        if not est.actividad2.presentada or est.actividad2.calificacion is None:
            motivos.append("El estudiante no ha presentado y calificado la actividad parcial del Módulo 2.")
        return motivos

    def _check_calificaciones_minimas(self, est: Estudiante) -> List[str]:
        motivos: List[str] = []
        if est.actividad1.calificacion is not None and est.actividad1.calificacion < 30:
            motivos.append("El estudiante no ha obtenido el puntaje mínimo de 30 puntos en la actividad parcial del Módulo 1.")
        if est.actividad2.calificacion is not None and est.actividad2.calificacion < 30:
            motivos.append("El estudiante no ha obtenido el puntaje mínimo de 30 puntos en la actividad parcial del Módulo 2.")
        return motivos

    # 4. Registro de asistencia
    def registrar_asistencia(self, identificacion: str, modulo_num: int, horas: float) -> Tuple[bool, str]:
        est = self.obtener_estudiante(identificacion)
        if not est:
            return False, MSG_ESTUDIANTE_NO_ENCONTRADO
        try:
            horasf = float(horas)
        except (TypeError, ValueError):
            return False, "Las horas deben ser un número válido."
        if horasf < 0:
            return False, "Las horas a registrar deben ser positivas."
        if horasf > 40:
            return False, "No se pueden registrar más de 40 horas en una sola entrada."
        if modulo_num == 1:
            return est.mod1.registrar_asistencia(horasf)
        elif modulo_num == 2:
            return est.mod2.registrar_asistencia(horasf)
        else:
            return False, "Número de módulo inválido."

    # 5. Registro de actividades parciales
    def registrar_actividad_parcial(self, identificacion: str, modulo_num: int, presentada: bool, calificacion: Optional[float]) -> Tuple[bool, str]:
        est = self.obtener_estudiante(identificacion)
        if not est:
            return False, MSG_ESTUDIANTE_NO_ENCONTRADO
        if presentada:
            if calificacion is None:
                return False, "Si la actividad fue presentada debe incluirse la calificación."
            try:
                cal = float(calificacion)
            except ValueError:
                return False, "La calificación debe ser un número."
            if cal < 0 or cal > 30:
                return False, "La calificación debe estar entre 0 y 30 puntos."
        else:
            cal = None

        if modulo_num == 1:
            est.actividad1.presentada = presentada
            est.actividad1.calificacion = cal
        elif modulo_num == 2:
            est.actividad2.presentada = presentada
            est.actividad2.calificacion = cal
        else:
            return False, "Número de módulo inválido."
        return True, "Registro de actividad parcial actualizado."

    # 6. Validación para el examen final
    def validar_habilitacion_examen(self, identificacion: str) -> Tuple[bool, List[str]]:
        est = self.obtener_estudiante(identificacion)
        if not est:
            return False, [MSG_ESTUDIANTE_NO_ENCONTRADO]

        motivos: List[str] = []
        motivos.extend(self._check_asistencias(est))
        motivos.extend(self._check_actividades_presentadas(est))
        motivos.extend(self._check_calificaciones_minimas(est))

        habilitado = len(motivos) == 0
        return habilitado, motivos

    # 7. Registrar examen final
    def registrar_examen_final(self, identificacion: str, calificacion: float) -> Tuple[bool, str]:
        est = self.obtener_estudiante(identificacion)
        if not est:
            return False, MSG_ESTUDIANTE_NO_ENCONTRADO
        habilitado, motivos = self.validar_habilitacion_examen(identificacion)
        if not habilitado:
            return False, "El estudiante no está habilitado para rendir el examen final: " + "; ".join(motivos)
        try:
            cal = float(calificacion)
        except ValueError:
            return False, "La calificación del examen debe ser un número."
        if cal < 0 or cal > 20:
            return False, "La calificación del examen debe estar entre 0 y 20 puntos."
        est.examen_final = round(cal, 2)
        return True, "Calificación del examen final registrada."

    # 7. Calificación final y reporte
    def calcular_calificacion_total(self, identificacion: str) -> Optional[float]:
        est = self.obtener_estudiante(identificacion)
        if not est:
            return None
        a1 = est.actividad1.calificacion or 0.0
        a2 = est.actividad2.calificacion or 0.0
        ef = est.examen_final or 0.0
        return round(a1 + a2 + ef, 2)

    def reporte_final(self, identificacion: str) -> Tuple[bool, str]:
        est = self.obtener_estudiante(identificacion)
        if not est:
            return False, MSG_ESTUDIANTE_NO_ENCONTRADO
        lines = []
        lines.append(f"Identificación: {est.identificacion}")
        lines.append(f"Nombre: {est.nombre_completo()}")
        lines.append(f"Curso: {est.curso}")
        lines.append(f"Horario: {HORARIO_NOMBRE.get(est.horario, est.horario)}")
        lines.append("")
        lines.append("--- Asistencia ---")
        lines.append(f"Módulo 1: {est.mod1.horas_asistidas}/{est.mod1.horas_programadas} horas (Faltantes: {est.mod1.horas_faltantes}) - {est.mod1.porcentaje_asistencia}%")
        lines.append(f"Módulo 2: {est.mod2.horas_asistidas}/{est.mod2.horas_programadas} horas (Faltantes: {est.mod2.horas_faltantes}) - {est.mod2.porcentaje_asistencia}%")
        lines.append("")
        lines.append("--- Actividades Parciales ---")
        if est.actividad1.presentada:
            lines.append(f"Actividad Módulo 1: Presentada - Calificación: {est.actividad1.calificacion}")
        else:
            lines.append("Actividad Módulo 1: No presentada")
        if est.actividad2.presentada:
            lines.append(f"Actividad Módulo 2: Presentada - Calificación: {est.actividad2.calificacion}")
        else:
            lines.append("Actividad Módulo 2: No presentada")
        lines.append("")
        habilitado, motivos = self.validar_habilitacion_examen(identificacion)
        if habilitado:
            lines.append("El estudiante cumple con los requisitos y está habilitado para rendir el examen final.")
        else:
            lines.append("El estudiante NO está habilitado para rendir el examen final por los siguientes motivos:")
            for m in motivos:
                lines.append(f"- {m}")
        lines.append("")
        lines.append(f"Calificación Examen Final: {est.examen_final if est.examen_final is not None else 'No registrada'}")
        lines.append(f"Calificación Total Acumulada: {self.calcular_calificacion_total(identificacion)}")

        return True, "\n".join(lines)


def mostrar_menu() -> None:
    sistema = SistemaCapacitacion()
    # configurar logging si no está configurado
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Intentar cargar datos previos
    ok, msg = sistema.load_from_file(DATA_FILE)
    if ok:
        logger.info(f"Datos cargados: {msg}")
    else:
        # Solo informar si existe archivo inválido; si no existe, no es error
        if os.path.exists(DATA_FILE):
            logger.warning(f"Aviso carga: {msg}")

    # Datos de prueba solicitados
    # Caso 1: Cumple todos los requisitos
    sistema.registrar_estudiante("1001", "Ana", "Gómez", DEFAULT_CURSO_PYTHON_BASICO, "M")
    sistema.registrar_asistencia("1001", 1, 15)
    sistema.registrar_asistencia("1001", 2, 15)
    sistema.registrar_actividad_parcial("1001", 1, True, 30)
    sistema.registrar_actividad_parcial("1001", 2, True, 30)
    sistema.registrar_examen_final("1001", 18)

    # Caso 2: No cumple asistencia mínima
    sistema.registrar_estudiante("1002", "Bruno", "Ruiz", DEFAULT_CURSO_PYTHON_BASICO, "T")
    sistema.registrar_asistencia("1002", 1, 14)
    sistema.registrar_asistencia("1002", 2, 16)
    sistema.registrar_actividad_parcial("1002", 1, True, 30)
    sistema.registrar_actividad_parcial("1002", 2, True, 30)

    # Caso 3: Cumple asistencia, pero no alcanza 30 en una actividad
    sistema.registrar_estudiante("1003", "Carla", "Méndez", DEFAULT_CURSO_PYTHON_BASICO, "M")
    sistema.registrar_asistencia("1003", 1, 16)
    sistema.registrar_asistencia("1003", 2, 16)
    sistema.registrar_actividad_parcial("1003", 1, True, 25)
    sistema.registrar_actividad_parcial("1003", 2, True, 30)

    # Interfaz simple de consola
    def _input_cedula() -> str:
        """Pide la cédula hasta que tenga 10 dígitos numéricos.

        Retorna la cédula válida como cadena.
        """
        while True:
            ced = input(PROMPT_CEDULA).strip()
            if not ced.isdigit() or len(ced) != 10:
                logger.warning("Cédula inválida. Debe contener 10 dígitos numéricos. Intente de nuevo.")
                continue
            if not validar_cedula_ecuador(ced):
                logger.warning("Cédula no consistente con parámetros válidos de cédula ecuatoriana. Intente de nuevo.")
                continue
            return ced
    def _menu_register_student() -> None:
        ced = _input_cedula()
        nom = input(PROMPT_NOMBRES).strip()
        ape = input(PROMPT_APELLIDOS).strip()
        curso = input(PROMPT_CURSO).strip()
        logger.info(PROMPT_HORARIOS)
        horario = input(PROMPT_SELECC_HORARIO).strip().upper()
        _, msg = sistema.registrar_estudiante(ced, nom, ape, curso, horario)
        logger.info(msg)

    def _menu_list_students() -> None:
        studs = sistema.consultar_estudiantes()
        if not studs:
            logger.info(MSG_NO_ESTUDIANTES)
            return
        for s in studs:
            logger.info(f"{s.identificacion} - {s.nombre_completo()} - {s.curso} - {HORARIO_NOMBRE.get(s.horario)}")

    def _menu_register_attendance() -> None:
        ced = _input_cedula()
        mod = input(PROMPT_MODULO).strip()
        horas = input(PROMPT_HORAS).strip()
        try:
            modn = int(mod)
            horasf = float(horas)
        except ValueError:
            logger.warning(MSG_VALORES_INVALIDOS_MODULO_HORAS)
            return
        _, msg = sistema.registrar_asistencia(ced, modn, horasf)
        logger.info(msg)

    def _menu_register_activity() -> None:
        ced = _input_cedula()
        mod = input(PROMPT_MODULO).strip()
        pres = input(PROMPT_PRESENTO).strip().upper()
        try:
            modn = int(mod)
        except ValueError:
            logger.warning(MSG_MODULO_INVALIDO)
            return
        presentada = pres == "S"
        cal = None
        if presentada:
            cal_in = input(PROMPT_CAL_030).strip()
            try:
                cal = float(cal_in)
            except ValueError:
                logger.warning(MSG_CALIFICACION_INVALIDA)
                return
        _, msg = sistema.registrar_actividad_parcial(ced, modn, presentada, cal)
        logger.info(msg)

    def _menu_consult_status() -> None:
        ced = _input_cedula()
        est = sistema.obtener_estudiante(ced)
        if not est:
            logger.info(MSG_ESTUDIANTE_NO_ENCONTRADO)
            return
        logger.info(f"Nombre: {est.nombre_completo()}")
        logger.info(f"Horario: {HORARIO_NOMBRE.get(est.horario)}")
        logger.info(f"Módulo 1 - Horas: {est.mod1.horas_asistidas} - Faltantes: {est.mod1.horas_faltantes} - %: {est.mod1.porcentaje_asistencia}")
        logger.info(f"Módulo 2 - Horas: {est.mod2.horas_asistidas} - Faltantes: {est.mod2.horas_faltantes} - %: {est.mod2.porcentaje_asistencia}")
        logger.info(f"Actividad 1: Presentada: {est.actividad1.presentada} - Calificación: {est.actividad1.calificacion}")
        logger.info(f"Actividad 2: Presentada: {est.actividad2.presentada} - Calificación: {est.actividad2.calificacion}")
        logger.info(f"Examen final: {est.examen_final}")

    def _menu_validate_habilitation() -> None:
        ced = _input_cedula()
        habilitado, motivos = sistema.validar_habilitacion_examen(ced)
        if habilitado:
            logger.info("El estudiante cumple con los requisitos y está habilitado para rendir el examen final.")
        else:
            logger.info("El estudiante no está habilitado por los siguientes motivos:")
            for m in motivos:
                logger.info(f"- {m}")

    def _menu_register_exam() -> None:
        ced = _input_cedula()
        cal_in = input("Calificación examen final (0-20): ").strip()
        try:
            cal = float(cal_in)
        except ValueError:
            logger.warning(MSG_CALIFICACION_INVALIDA)
            return
        _, msg = sistema.registrar_examen_final(ced, cal)
        logger.info(msg)

    def _menu_report() -> None:
        ced = _input_cedula()
        ok, reporte = sistema.reporte_final(ced)
        if not ok:
            logger.error(reporte)
        else:
            logger.info(reporte)

    while True:
        logger.info("\n--- Sistema de Capacitación ---")
        logger.info("1. Registrar estudiante")
        logger.info("2. Consultar estudiantes")
        logger.info("3. Registrar asistencia")
        logger.info("4. Registrar actividad parcial")
        logger.info("5. Consultar estado académico del estudiante")
        logger.info("6. Validar habilitación para examen final")
        logger.info("7. Registrar examen final")
        logger.info("8. Mostrar reporte final del estudiante")
        logger.info("9. Salir")
        opcion = input(PROMPT_SELECT_OPTION).strip()
        if opcion == "1":
            _menu_register_student()
        elif opcion == "2":
            _menu_list_students()
        elif opcion == "3":
            _menu_register_attendance()
        elif opcion == "4":
            _menu_register_activity()
        elif opcion == "5":
            _menu_consult_status()
        elif opcion == "6":
            _menu_validate_habilitation()
        elif opcion == "7":
            _menu_register_exam()
        elif opcion == "8":
            _menu_report()
        elif opcion == "9":
            logger.info("Guardando datos y saliendo...")
            ok, msg = sistema.save_to_file(DATA_FILE)
            if ok:
                logger.info(msg)
            else:
                logger.error(f"Error al guardar datos: {msg}")
            break
        else:
            logger.warning(MSG_OPCION_INVALIDA)


if __name__ == "__main__":
    mostrar_menu()
