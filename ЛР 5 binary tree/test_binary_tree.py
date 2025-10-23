import unittest

from main import gen_bin_tree

class TestSumma(unittest.TestCase):
    def test_correct_variant(self):
        self.assertEqual(gen_bin_tree(), {'2': [{'6': [{'18': [{'54': [{'162': [{'486': []}, {'166': []}]}, {'58': [{'174': []}, {'62': []}]}]}, {'22': [{'66': [{'198': []}, {'70': []}]}, {'26': [{'78': []}, {'30': []}]}]}]}, {'10': [{'30': [{'90': [{'270': []}, {'94': []}]}, {'34': [{'102': []}, {'38': []}]}]}, {'14': [{'42': [{'126': []}, {'46': []}]}, {'18': [{'54': []}, {'22': []}]}]}]}]}, {'6': [{'18': [{'54': [{'162': [{'486': []}, {'166': []}]}, {'58': [{'174': []}, {'62': []}]}]}, {'22': [{'66': [{'198': []}, {'70': []}]}, {'26': [{'78': []}, {'30': []}]}]}]}, {'10': [{'30': [{'90': [{'270': []}, {'94': []}]}, {'34': [{'102': []}, {'38': []}]}]}, {'14': [{'42': [{'126': []}, {'46': []}]}, {'18': [{'54': []}, {'22': []}]}]}]}]}]})


    def test_correct(self):
        """Тест с нецелым корнем"""
        self.assertEqual(gen_bin_tree(5, 2.1, l_leaf=lambda x: x+2, r_leaf=lambda y: y*5), {'2.1': [{'4.1': [{'6.1': [{'8.1': [{'10.1': []}, {'40.5': []}]}, {'30.5': [{'32.5': []}, {'152.5': []}]}]}, {'20.5': [{'22.5': [{'24.5': []}, {'112.5': []}]}, {'102.5': [{'104.5': []}, {'512.5': []}]}]}]}, {'10.5': [{'12.5': [{'14.5': [{'16.5': []}, {'72.5': []}]}, {'62.5': [{'64.5': []}, {'312.5': []}]}]}, {'52.5': [{'54.5': [{'56.5': []}, {'272.5': []}]}, {'262.5': [{'264.5': []}, {'1312.5': []}]}]}]}]})



    def test_float_height(self):
        """Тест с нецелой высотой"""
        with self.assertRaises(TypeError):
            gen_bin_tree(4.1, 2, l_leaf=lambda x: x*2, r_leaf=lambda y: y+3)


    def test_string_height(self):
        """Тест с высотой-строкой"""
        with self.assertRaises(TypeError):
            gen_bin_tree('4', 2, l_leaf=lambda x: x*2, r_leaf=lambda y: y+3)

    def test_string_root(self):
        """Тест с корнем-строкой"""
        with self.assertRaises(TypeError):
            gen_bin_tree(4, '2', l_leaf=lambda x: x*2, r_leaf=lambda y: y+3)

    def test_zero_root(self):
        """Тест с нулевым корнем"""
        self.assertEqual(gen_bin_tree(3, 0, l_leaf=lambda x: x*2, r_leaf=lambda y: y+3), {'0': [{'0': [{'0': []}, {'3': []}]}, {'3': [{'6': []}, {'6': []}]}]})

    def test_zero_height(self):
        """Тест с нулевой высотой"""
        self.assertEqual(gen_bin_tree(0, 3, l_leaf=lambda x: x*2, r_leaf=lambda y: y+3), {})

    def test_one_height(self):
        """Тест с высотой равной 1"""
        self.assertEqual(gen_bin_tree(1, 3, l_leaf=lambda x: x*2, r_leaf=lambda y: y+3), {'3': []})

    def test_negative_height(self):
        """Тест с отрикательной высотой"""
        with self.assertRaises(TypeError):
            gen_bin_tree(-5, 3, l_leaf=lambda x: x*2, r_leaf=lambda y: y+3)

    def test_large_height(self):
        """Тест с большой высотой"""
        self.assertIsInstance(gen_bin_tree(10, 1, l_leaf=lambda x: x, r_leaf=lambda y: y), dict)

    def test_string_lambda(self):
        """Тест с функцией-строкой"""
        with self.assertRaises(TypeError):
            gen_bin_tree(10, 1, l_leaf=lambda x: x+'5', r_leaf=lambda y: y)
