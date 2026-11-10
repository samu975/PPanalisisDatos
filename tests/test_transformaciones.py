import unittest

from transformaciones import a_pesos, a_porcentaje, marca_desde_nombre


class TransformacionesTest(unittest.TestCase):
    def test_pesos(self):
        self.assertEqual(a_pesos("$ 2.499.900"), 2499900)
        self.assertIsNone(a_pesos(None))
        self.assertIsNone(a_pesos("sin precio"))

    def test_porcentaje(self):
        self.assertEqual(a_porcentaje("Ahorra 25 %"), 25)
        self.assertEqual(a_porcentaje(None), 0)

    def test_marcas_y_alias(self):
        for nombre, esperado in [("Portátil Lenovo IdeaPad", "LENOVO"), ("MacBook Air", "APPLE"), ("OmniBook X", "HP"), ("Equipo desconocido", "OTRA"), (None, "OTRA")]:
            with self.subTest(nombre=nombre):
                self.assertEqual(marca_desde_nombre(nombre), esperado)


if __name__ == "__main__":
    unittest.main()
