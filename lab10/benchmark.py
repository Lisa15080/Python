# benchmark.py
import time
import math
import concurrent.futures as ftres
from core import integrate, integrate_async, integrate_mp
from cintegrate import integrate_cython_sin, integrate_cython_sin_nogil_wrapper

def time_it(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    return result, time.perf_counter() - start

def _cython_worker(args):
    a_i, b_i, n_i = args
    return integrate_cython_sin(a_i, b_i, n_i)

def _cython_nogil_worker(args):
    a_i, b_i, n_i = args
    return integrate_cython_sin_nogil_wrapper(a_i, b_i, n_i)

def benchmark_cython():
    a, b = 0.0, math.pi
    n_iter = 10_000_000
    f = math.sin

    print("Сравнение производительности: Python или Cython (с потоками и процессами)")
    print(f"Функция: sin(x), Интервал: [0, π], n_iter = {n_iter:,}")

    # Python
    res, t = time_it(integrate, f, a, b, n_iter=n_iter)
    print(f"python: n_jobs=1, время={t:.4f} сек, результат={res:.5f}")

    # Threads
    for n in [2, 4, 6, 8]:
        res, t = time_it(integrate_async, f, a, b, n_jobs=n, n_iter=n_iter)
        print(f"threads: n_jobs={n}, время={t:.4f} сек, результат={res:.5f}")

    # Processes
    for n in [2, 4, 6, 8]:
        res, t = time_it(integrate_mp, f, a, b, n_jobs=n, n_iter=n_iter)
        print(f"processes: n_jobs={n}, время={t:.4f} сек, результат={res:.5f}")

    # Cython
    res, t = time_it(integrate_cython_sin, a, b, n_iter)
    print(f"cython: n_jobs=1, время={t:.4f} сек, результат={res:.5f}")

    # Cython + Threads (8)
    n_jobs = 8
    step = (b - a) / n_jobs
    base = n_iter // n_jobs
    remainder = n_iter % n_jobs
    tasks = [(a + i * step, a + (i + 1) * step, base + (1 if i < remainder else 0))
             for i in range(n_jobs)]

    with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        start = time.perf_counter()
        total = sum(executor.map(_cython_worker, tasks))
        t = time.perf_counter() - start
    print(f"cython + threads: n_jobs={n_jobs}, время={t:.4f} сек, результат={total:.5f}")

    # Cython + Processes (8)
    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        start = time.perf_counter()
        total = sum(executor.map(_cython_worker, tasks))
        t = time.perf_counter() - start
    print(f"cython + processes: n_jobs={n_jobs}, время={t:.4f} сек, результат={total:.5f}")

    print(f"\nТочное значение интеграла: {2.0:.6f}\n")

def benchmark_no_gil():
    a, b = 0.0, math.pi
    n_iter = 10_000_000
    n_jobs_list = [2, 4, 6]

    print("Многопоточность в Cython с noGIL")
    print(f"Функция: sin(x), n_iter = {n_iter:,}")

    # Однопоточный noGIL
    res, t = time_it(_cython_nogil_worker, (a, b, n_iter))
    print(f"cython (noGIL): n_jobs=1, время={t:.4f} сек, результат={res:.5f}")

    # Многопоточный noGIL
    total_interval = b - a
    for n_jobs in n_jobs_list:
        step = total_interval / n_jobs
        base = n_iter // n_jobs
        remainder = n_iter % n_jobs
        tasks = [(a + i * step, a + (i + 1) * step, base + (1 if i < remainder else 0))
                 for i in range(n_jobs)]
        start = time.perf_counter()
        with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
            total = sum(executor.map(_cython_nogil_worker, tasks))
        t = time.perf_counter() - start
        print(f"cython nogil threads: n_jobs={n_jobs}, время={t:.4f} сек, результат={total:.5f}")

    # Сравнение с процессами
    n_jobs = 6
    step = total_interval / n_jobs
    base = n_iter // n_jobs
    remainder = n_iter % n_jobs
    tasks = [(a + i * step, a + (i + 1) * step, base + (1 if i < remainder else 0))
             for i in range(n_jobs)]
    start = time.perf_counter()
    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        total = sum(executor.map(_cython_worker, tasks))
    t = time.perf_counter() - start
    print(f"cython processes: n_jobs={n_jobs}, время={t:.4f} сек, результат={total:.5f}")

    print(f"\nТочное значение: {2.0:.6f}")

def run_all_benchmarks():
    benchmark_cython()
    benchmark_no_gil()
