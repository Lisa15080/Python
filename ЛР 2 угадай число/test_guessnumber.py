import unittest

from main import main
from main import input_of_numbers
from main import random_numbers


class TestSumma(unittest.TestCase):

    # тесты для корректных данных
    def test_correct_1(self):
        self.assertEqual(main(2, 'seq', 1, 5), [2, 2])

    def test_correct_2(self):
        self.assertEqual(main(7, 'bin', 1, 10), [7, 4])

    def test_correct_3(self):
        self.assertEqual(main(5, 'seq', 6, 20), [None, 15])
        