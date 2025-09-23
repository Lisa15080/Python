import unittest

from main import summa


class TestSumma(unittest.TestCase):

    # тесты для корректных данных, предоставленных преподавателем
    def test_correct_sum(self):
        self.assertEqual(summa([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(summa([3, 2, 4], 6), [1, 2])
        self.assertEqual(summa([3, 3], 6), [0, 1])

    # тесты для других случаев корректных данных
    def test_my_sum1(self):
        self.assertEqual(summa([-4, -2, 6], -6), [0, 1])

    def test_my_sum2(self):
        self.assertEqual(summa([1, 1, 1], 2), [0, 1])

    def test_my_sum3(self):
        self.assertEqual(summa([0, 100_000, 200_000, 100_000, 200_000], 300_000), [1, 2])

    def test_my_sum4(self):
        self.assertEqual(summa([-1, 2, 5, 2], 4), [0, 2])


    def test_not_possible_target(self): #проверка, вернет ли None, если невозможно получить target
        self.assertEqual(summa([-1, 2, 5, 2], 10), None)

    # тесты для некорректных данных
    def test_empty_list(self): #проверка, вернет ли ошибку, если введен пустой список
        with self.assertRaises(TypeError):
            summa([], 0)

    def test_with_float(self): #проверка, вернет ли ошибку, если в списке будут дробные числа
        with self.assertRaises(TypeError):
            summa([2, 2.5], 4.5)

    def test_with_string(self): #проверка, вернет ли ошибку, если число будет представлено в строковом формате
        with self.assertRaises(TypeError):
            summa([2, '2'], 4)


    def test_string_target(self): #проверка, вернет ли ошибку, если target - строка
        with self.assertRaises(TypeError):
            summa([2, 3], '5')

    def test_float_target(self): #проверка, вернет ли ошибку, если target - нецелое число
        with self.assertRaises(TypeError):
            summa([2, 3], 5.1)



if __name__ == '__main__':
    # unittest.main()
    unittest.main(argv=[''], verbosity=2, exit=False)
