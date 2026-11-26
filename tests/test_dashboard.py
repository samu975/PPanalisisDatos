import unittest
from seguimiento.actualizar import generar


class DashboardTest(unittest.TestCase):
    def test_informe_muestra_fecha_y_escapa_contenido(self):
        producto = {'codigo': '199642458734', 'nombre': 'HP <equipo>', 'marca': 'HP', 'precio_cop': 2000000}
        salida = generar([producto], 1, '2026-11-25 10:00:00')
        self.assertIn('2026-11-25 10:00:00', salida)
        self.assertIn('HP &lt;equipo&gt;', salida)
        self.assertIn('$2.000.000', salida)
        self.assertNotIn('HP <equipo>', salida)

    def test_destacado_ausente(self):
        salida = generar([{'codigo': '1', 'nombre': 'Equipo', 'marca': 'OTRA', 'precio_cop': 50}], 1, 'fecha')
        self.assertIn('no apareció', salida)
