# import time
# import threading
#
# def countdown(n):
#     for i in range(n):
#         print(f'{n-i-1} left')
#         time.sleep(1)
#
# t=threading.Thread(target = countdown, args = (5,))
# print("Hello 1")
# t.start()
# t.join()
# print('Hello 2')
import threading
import time


# class CountdowmThread(threading.Thread):
#     def __init__(self, n):
#         super().__init__()
#         self.n=n
#
#     def run(self):
#         for i in range(self.n):
#             print(self.n-i-1, "left")
#             time.sleep(1)
#
# t=CountdowmThread(3)
# print("Hello 1")
# t.start()
# print("Hello 2")

# import time
# import threading
#
# t = threading.Thread(target=time.sleep, args=(3,), daemon=True)
# t.start()
# print('Q: Are daemons exist?\nA: {}'.format(t.is_alive()))
# time.sleep(0.1)
# print('Q: Are daemons exist?\nA: {}'.format(t.is_alive()))

from

