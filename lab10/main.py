# main.py
import doctest

if __name__ == '__main__':
    doctest.testmod(verbose=False)

    from benchmark import run_all_benchmarks
    run_all_benchmarks()


#  # main.py
# import math
# import doctest
# import unittest
# import time
# import concurrent.futures as ftres
# from core import integrate, integrate_async, integrate_mp
#
# # Вспомогательная функция для ProcessPoolExecutor (должна быть глобальной!)
# def _cython_worker(args):
#     a_i, b_i, n_i = args
#     from cintegrate import integrate_cython_sin
#     return integrate_cython_sin(a_i, b_i, n_i)
#
# # Для многопоточного Cython с noGIL
# def _cython_nogil_worker(args):
#     a_i, b_i, n_i = args
#     from cintegrate import integrate_cython_sin_nogil_wrapper
#     return integrate_cython_sin_nogil_wrapper(a_i, b_i, n_i)
#
# # Импорт Cython-функции (должна быть собрана!)
# from cintegrate import integrate_cython_sin
#
# # ===============
# # Вспомогательные функции
# # ===============
# def time_it(func, *args, **kwargs):
#     start = time.perf_counter()
#     result = func(*args, **kwargs)
#     end = time.perf_counter()
#     return result, end - start
#
# # ===============
# # Бенчмарк для итерации 4
# # ===============
# def benchmark_iteration_4():
#     a, b = 0.0, math.pi
#     n_iter = 10_000_000  # достаточно большой объём
#     f = math.sin
#
#     print("Итерация 4: Профилирование и оптимизация с Cython")
#     print(f"Функция: sin(x), Интервал: [0, π], n_iter = {n_iter:,}")
#     print(f"{'Метод':<20} | {'n_jobs':<7} | {'Время (сек)':<12} | {'Результат':<10}")
#     print("-" * 65)
#
#     # 1. Python (sequential)
#     res, t = time_it(integrate, f, a, b, n_iter=n_iter)
#     print(f"{'python':<20} | {'1':<7} | {t:<12.4f} | {res:<10.5f}")
#
#     # 2. Threads (2, 4, 6, 8)
#     for n in [2, 4, 6, 8]:
#         res, t = time_it(integrate_async, f, a, b, n_jobs=n, n_iter=n_iter)
#         print(f"{'threads':<20} | {n:<7} | {t:<12.4f} | {res:<10.5f}")
#
#     # 3. Processes (2, 4, 6, 8)
#     for n in [2, 4, 6, 8]:
#         res, t = time_it(integrate_mp, f, a, b, n_jobs=n, n_iter=n_iter)
#         print(f"{'processes':<20} | {n:<7} | {t:<12.4f} | {res:<10.5f}")
#
#     # 4. Cython (без параллелизма)
#     res, t = time_it(integrate_cython_sin, a, b, n_iter)
#     print(f"{'cython':<20} | {'1':<7} | {t:<12.4f} | {res:<10.5f}")
#
#     # 5. Cython + Threads (8)
#     n_jobs = 8
#     step = (b - a) / n_jobs
#     base = n_iter // n_jobs
#     remainder = n_iter % n_jobs
#     tasks = [
#         (a + i * step, a + (i + 1) * step, base + (1 if i < remainder else 0))
#         for i in range(n_jobs)
#     ]
#
#     with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
#         start = time.perf_counter()
#         results = executor.map(_cython_worker, tasks)
#         total = sum(results)
#         t = time.perf_counter() - start
#     print(f"{'cython + threads':<20} | {n_jobs:<7} | {t:<12.4f} | {total:<10.5f}")
#
#     # 6. Cython + Processes (8)
#     with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
#         start = time.perf_counter()
#         results = executor.map(_cython_worker, tasks)
#         total = sum(results)
#         t = time.perf_counter() - start
#     print(f"{'cython + processes':<20} | {n_jobs:<7} | {t:<12.4f} | {total:<10.5f}")
#
# def benchmark_iteration_5():
#     """Итерация 5: Cython с noGIL + сравнение с процессами."""
#     a, b = 0.0, math.pi
#     n_iter = 10_000_000
#     n_jobs_list = [2, 4, 6]
#
#     print("\nИтерация 5: Cython с noGIL")
#     print(f"Функция: sin(x), n_iter = {n_iter:,}")
#     print(f"{'Метод':<20} | {'n_jobs':<7} | {'Время (сек)':<12} | {'Результат':<10}")
#     print("-" * 65)
#
#     # Однопоточный noGIL (база)
#     res, t = time_it(_cython_nogil_worker, (a, b, n_iter))
#     print(f"{'cython (noGIL)':<20} | {'1':<7} | {t:<12.4f} | {res:<10.5f}")
#
#     # Многопоточный noGIL
#     step = (b - a) / max(n_jobs_list)
#     for n_jobs in n_jobs_list:
#         base = n_iter // n_jobs
#         remainder = n_iter % n_jobs
#         tasks = [
#             (a + i * step, a + (i + 1) * step, base + (1 if i < remainder else 0))
#             for i in range(n_jobs)
#         ]
#         start = time.perf_counter()
#         with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
#             results = executor.map(_cython_nogil_worker, tasks)
#             total = sum(results)
#         t = time.perf_counter() - start
#         print(f"{'cython noGIL threads':<20} | {n_jobs:<7} | {t:<12.4f} | {total:<10.5f}")
#
#     # Сравнение: Cython + процессы (из итерации 4)
#     n_jobs = 6
#     base = n_iter // n_jobs
#     remainder = n_iter % n_jobs
#     tasks = [
#         (a + i * step, a + (i + 1) * step, base + (1 if i < remainder else 0))
#         for i in range(n_jobs)
#     ]
#     start = time.perf_counter()
#     with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
#         results = executor.map(_cython_worker, tasks)
#         total = sum(results)
#     t = time.perf_counter() - start
#     print(f"{'cython processes':<20} | {n_jobs:<7} | {t:<12.4f} | {total:<10.5f}")
#
#     print(f"\nТочное значение: {2.0:.6f}")
#
#
# if __name__ == '__main__':
#     # Запуск doctest и unittest
#     doctest.testmod(verbose=False)
#
#     print("=" * 65)
#     benchmark_iteration_4()
#
#     print("=" * 65)
#     benchmark_iteration_5()

