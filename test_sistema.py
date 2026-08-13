import unittest
from sistema_capacitacion import SistemaCapacitacion


class TestSistemaCapacitacion(unittest.TestCase):
    def test_caso_1_habilitado_y_examen_registrable(self):
        s = SistemaCapacitacion()
        s.registrar_estudiante("1001", "Ana", "Gómez", "Python Básico", "M")
        s.registrar_asistencia("1001", 1, 15)
        s.registrar_asistencia("1001", 2, 15)
        s.registrar_actividad_parcial("1001", 1, True, 30)
        s.registrar_actividad_parcial("1001", 2, True, 30)
        habilitado, motivos = s.validar_habilitacion_examen("1001")
        self.assertTrue(habilitado)
        ok, msg = s.registrar_examen_final("1001", 19)
        self.assertTrue(ok)
        total = s.calcular_calificacion_total("1001")
        self.assertEqual(total, 30 + 30 + 19)

    def test_caso_2_no_cumple_asistencia(self):
        s = SistemaCapacitacion()
        s.registrar_estudiante("1002", "Bruno", "Ruiz", "Python Básico", "T")
        s.registrar_asistencia("1002", 1, 14)
        s.registrar_asistencia("1002", 2, 16)
        s.registrar_actividad_parcial("1002", 1, True, 30)
        s.registrar_actividad_parcial("1002", 2, True, 30)
        habilitado, motivos = s.validar_habilitacion_examen("1002")
        self.assertFalse(habilitado)
        self.assertIn("Módulo 1", "; ".join(motivos))
        ok, msg = s.registrar_examen_final("1002", 18)
        self.assertFalse(ok)

    def test_caso_3_actividad_no_alcanza_30(self):
        s = SistemaCapacitacion()
        s.registrar_estudiante("1003", "Carla", "Méndez", "Python Básico", "M")
        s.registrar_asistencia("1003", 1, 16)
        s.registrar_asistencia("1003", 2, 16)
        s.registrar_actividad_parcial("1003", 1, True, 25)
        s.registrar_actividad_parcial("1003", 2, True, 30)
        habilitado, motivos = s.validar_habilitacion_examen("1003")
        self.assertFalse(habilitado)
        self.assertTrue(any("puntaje mínimo" in m for m in motivos))
        ok, msg = s.registrar_examen_final("1003", 15)
        self.assertFalse(ok)


if __name__ == '__main__':
    unittest.main()
