import random
import time
from algorithms import randomized_quicksort, deterministic_quicksort


def make_random_list(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


def make_sorted_list(n):
    return list(range(n))


def make_reverse_sorted_list(n):
    return list(range(n, 0, -1))


def make_repeated_list(n):
    return [random.randint(0, max(5, n // 20)) for _ in range(n)]


def average_runtime(sort_fn, builder, n, trials=5):
    durations = []

    for _ in range(trials):
        data = builder(n)
        start = time.perf_counter()
        output = sort_fn(data)
        elapsed = time.perf_counter() - start
        assert output == sorted(data)
        durations.append(elapsed)

    return sum(durations) / len(durations)


def main():
    sizes = [1000, 2000, 4000, 8000]
    scenarios = {
        "Random": make_random_list,
        "Sorted": make_sorted_list,
        "Reverse Sorted": make_reverse_sorted_list,
        "Repeated Elements": make_repeated_list,
    }

    print("Average runtime in seconds")
    print("-" * 60)

    for label, builder in scenarios.items():
        print(f"\nScenario: {label}")
        print(f"{'n':>8} {'Randomized':>15} {'Deterministic':>15}")

        for n in sizes:
            r_time = average_runtime(randomized_quicksort, builder, n)
            d_time = average_runtime(deterministic_quicksort, builder, n)
            print(f"{n:>8} {r_time:>15.6f} {d_time:>15.6f}")


if __name__ == "__main__":
    main()

