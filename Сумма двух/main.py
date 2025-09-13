# def summa(nums, target):
#     for x in nums:
#         if int(x)!=x or str(x)==x:
#             return None
#     for i in range(len(nums) - 1):
#         for j in range(i + 1, len(nums)):
#             if nums[i] + nums[j] == target:
#                 return [i, j]
#
# print(summa([3, '3'], 6))

# def summa(nums, target):
#     for i in range(len(nums) - 1):
#         for j in range(i + 1, len(nums)):
#             if float(nums[i]) + float(nums[j]) == target:
#                 return [i, j]
#
# print(summa([3, '3.1'], 6))


import unittest
class TestMath(unittest.TestCase):
    def summa(nums):
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):


    def test(self):
        self.assertEqual()