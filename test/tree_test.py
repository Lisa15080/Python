import unittest
from tree import gen_bin_tree
class TestMath(unittest.TestCase):
  def test_height_1(self):
        """Тест минимальной высоты 1"""
        result = gen_bin_tree(1, 10)
        expected = {'10': []}
        self.assertEqual(result, expected)

  def test_height_0(self):
        """Тест нулевой высоты"""
        result = gen_bin_tree(0, 5)
        expected = {'5': []}
        self.assertEqual(result, expected)