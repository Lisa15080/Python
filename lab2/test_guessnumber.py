
import unittest

from main import main
from main import input_of_numbers
from main import random_numbers
from unittest.mock import patch


class TestSumma(unittest.TestCase):

    # Тесты для main
    def test_correct_1(self):
        """Тест main с корректными значениями, последовательный поиск"""
        self.assertEqual(main(2, 'seq', 1, 5), [2, 2])

    def test_correct_2(self):
        """Тест main с корректными значениями, бинарный поиск"""
        self.assertEqual(main(7, 'bin', 1, 10), [7, 4])

    def test_negative_num(self):
        """Тест main с отрицательным диапазоном"""
        self.assertEqual(main(-9, 'bin', -10, -2), [-9, 2])

    def test_many_num(self):
        """Тест main с большим диапазоном"""
        self.assertEqual(main(576, 'bin', 0, 1000), [576, 10])

    def test_not_found_target(self):
        """Тест main при отсутствии target в списке, последовательный поиск"""
        self.assertEqual(main(5, 'seq', 6, 20), [None, 15])

    def test_main_empty_list(self):
        """Тест main с некорректным значением start и end"""
        with self.assertRaises(ValueError):
            main(6, 'bin', 8, 6)

    def test_main_string_target(self):
        """Тест main с target-строкой"""
        with self.assertRaises(TypeError):
            input_of_numbers('7', 'bin')

    def test_invalid_search_type(self):
        """Тест с неверным типом поиска"""
        with self.assertRaises(TypeError):
            main(5, 'incorrect', 1, 10)

    def test_len_list_1(self):
        """Тест с длиной диапазона равной 1"""
        self.assertEqual(main(1, 'bin', 1, 1), [1, 1])

    #Тесты для input_of_numbers
    def test_input_seq(self):
        """Тест ввода чисел пользователем, последовательный поиск"""
        # Имитируем ввод: 5 чисел [1, 3, 5, 7, 9], ищем 5
        with patch('builtins.input', side_effect=['5', '1', '3', '5', '7', '9']):
            result = input_of_numbers(5, 'seq')
            self.assertEqual(result, [5, 3])

    def test_input_target_not_found(self):
        """Тест ввода чисел пользователем с отсутствием target в списке"""
        # Имитируем ввод: 5 чисел [1, 3, 5, 7, 9], ищем 4
        with patch('builtins.input', side_effect=['5', '1', '3', '5', '7', '9']):
            result = input_of_numbers(4, 'bin')
            self.assertEqual(result, [None, 3])  # Не найден, 1 попытка

    def test_input_negative_numbers(self):
        """Тест ввода отрицательных чисел"""
        with patch('builtins.input', side_effect=['4', '-5', '-3', '0', '2']):
            result = input_of_numbers(-3, 'bin')
            self.assertEqual(result, [-3, 1])





    #Тесты для random_numbers
    @patch('main.random.randint')
    def test_random_numbers(self, mock_randint):
        """Тест random_numbers"""
        mock_randint.side_effect = [5, 2, 8, 1, 9]
        result = random_numbers(8, 'seq', 1, 10, 5)
        self.assertEqual(result, [8, 3])

    @patch('main.random.randint')
    def test_random_duplicates_binary(self, mock_randint):
        """Тест бинарного поиска с дубликатами"""
        mock_randint.side_effect = [5, 5, 3, 3, 1]
        result = random_numbers(3, 'bin', 1, 10, 5)
        self.assertEqual(result, [3, 1])


    @patch('main.random.randint')
    def test_random_duplicates_binary(self, mock_randint):
        """Тест бинарного поиска с отсутствием значений в диапазоне"""
        mock_randint.side_effect = [5, 3, 1, 7, 8]
        result = random_numbers(2, 'bin', 1, 10, 5)
        self.assertEqual(result, [None, 3])


