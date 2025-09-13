from __future__ import annotations

import argparse
import random
import timeit
import csv
from typing import List, Callable, Dict, Tuple

def insertion_sort(arr: List[int]) -> List[int]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]:
    result: List[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def timsort(arr: List[int]) -> List[int]:
    return sorted(arr)

def make_data(kind: str, n: int, seed: int = 42) -> List[int]:
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(0, 10**9) for _ in range(n)]
    elif kind == "sorted":
        return list(range(n))
    elif kind == "reversed":
        return list(range(n, 0, -1))
    elif kind == "almost":
        a = list(range(n))
        k = max(1, n // 10)
        for _ in range(k):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    else:
        raise ValueError(f"Невідомий тип даних: {kind}")

def time_algorithm(func: Callable[[List[int]], List[int]], data: List[int], repeats: int) -> float:
    t = timeit.timeit(lambda: func(data), number=repeats)
    return t / repeats

def run_bench(sizes, kinds, repeats):
    algos: Dict[str, Callable[[List[int]], List[int]]] = {
        "Insertion": insertion_sort,
        "Merge": merge_sort,
        "Timsort": timsort,
    }
    records = []
    headers = ["algo", "kind", "n", "avg_sec"]
    for n in sizes:
        for kind in kinds:
            base = make_data(kind, n, seed=123)
            for name, fn in algos.items():
                avg = time_algorithm(fn, base, repeats=repeats)
                records.append((name, kind, n, avg))
    return headers, records

def main():
    parser = argparse.ArgumentParser(description="Порівняння сортувань (Insertion vs Merge vs Timsort) з timeit.")
    parser.add_argument("--sizes", type=int, nargs="+", default=[1000, 5000, 10000], help="Розміри масивів")
    parser.add_argument("--kinds", type=str, nargs="+", default=["random", "sorted", "reversed", "almost"], help="Типи наборів")
    parser.add_argument("--repeats", type=int, default=3, help="Кількість повторів для усереднення")
    parser.add_argument("--save-csv", type=str, default="", help="Шлях для збереження CSV")
    args = parser.parse_args()

    headers, rows = run_bench(args.sizes, args.kinds, args.repeats)

    colw = [10, 9, 8, 12]
    print(f"{headers[0]:<{colw[0]}} {headers[1]:<{colw[1]}} {headers[2]:>{colw[2]}} {headers[3]:>{colw[3]}}")
    for algo, kind, n, avg in rows:
        print(f"{algo:<{colw[0]}} {kind:<{colw[1]}} {n:>{colw[2]}} {avg:>{colw[3]}.6f}")

    if args.save_csv:
        with open(args.save_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            for r in rows:
                w.writerow(r)
        print(f"\nCSV збережено до: {args.save_csv}")

if __name__ == "__main__":
    main()
