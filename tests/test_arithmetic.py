import importlib.util
import os
import unittest


def load_arith_module():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    mod_path = os.path.join(root, "PythonBasics", "ArithmeticOperation.py")
    spec = importlib.util.spec_from_file_location("arith", mod_path)
    arith = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arith)
    return arith


class TestArithmeticFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arith = load_arith_module()

    def test_add(self):
        self.assertEqual(self.arith.add(1, 2, 3), 6)

    def test_subtract(self):
        self.assertEqual(self.arith.subtract(10, 1, 2), 7)

    def test_multiply(self):
        self.assertEqual(self.arith.multiply(2, 3, 4), 24)

    def test_divide(self):
        self.assertAlmostEqual(self.arith.divide(20, 2, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.arith.divide(1, 0)

    def test_power(self):
        self.assertEqual(self.arith.power(2, 3), 8)

    def test_modulo(self):
        self.assertEqual(self.arith.modulo(10, 3), 1)

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.arith.modulo(10, 0)


if __name__ == "__main__":
    unittest.main()
