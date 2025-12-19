# test.py
import unittest
import math
from core import integrate  # Рекомендуется импортировать из core, а не из main

class TestIntegrate(unittest.TestCase):

    def test_integrate_cos_0_to_pi(self):
        """Интеграл cos(x) от 0 до pi = 0"""
        result = integrate(math.cos, 0, math.pi, n_iter=100000)
        self.assertAlmostEqual(result, 0.0, places=3)

    def test_integrate_sin_0_to_pi(self):
        """Интеграл sin(x) от 0 до pi = 2"""
        result = integrate(math.sin, 0, math.pi, n_iter=100000)
        self.assertAlmostEqual(result, 2.0, places=3)

    def test_integrate_tan_0_to_pi_over_4(self):
        """Интеграл tan(x) от 0 до pi/4 = 0.5 * ln(2) ≈ 0.34657"""
        result = integrate(math.tan, 0, math.pi / 4, n_iter=100000)
        expected = 0.5 * math.log(2)
        self.assertAlmostEqual(result, expected, places=3)

    def test_convergence_with_n_iter(self):
        """
        Проверка устойчивости при увеличении числа итераций.
        """
        f = math.sin
        a, b = 0.0, math.pi
        exact = 2.0

        # Маленькое число итераций
        n_low = 10000
        result_low = integrate(f, a, b, n_iter=n_low)
        error_low = abs(result_low - exact)

        # Большое число итераций
        n_high = 2000000
        result_high = integrate(f, a, b, n_iter=n_high)
        error_high = abs(result_high - exact)

        # Ошибка при большем n_iter должна быть меньше
        self.assertLess(
            error_high,
            error_low,
            msg=f"Ошибка при n={n_high} ({error_high:.6f}) "
                f"не меньше ошибки при n={n_low} ({error_low:.6f})"
        )

        self.assertAlmostEqual(result_high, exact, places=4)