import random
import time
from algorithms import randomized_quicksort, deterministic_quicksort


# Generates a list with random values
def make_random_list(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


# Generates an already sorted list
def make_sorted_list(n):
    return list(range(n))


# Generates a reverse sorted list
# Useful to test worst-case behavior of deterministic quicksort
def make_reverse_sorted_list(n):
    return list(range(n, 0, -1))


# Generates a list with many repeated elements
# This helps test how algorithms handle duplicates
def make_repeated_list(n):
    return [random.randint(0, max(5, n // 20)) for _ in range(n)]


# Measures average runtime for a sorting function
# Runs the same test multiple times and returns the average
def average_runtime(sort_fn, builder, n, trials=5):
    durations = []

    for _ in range(trials):
        # Generate input data using provided builder function
        data = builder(n)

        # Start timer
        start = time.perf_counter()

        # Run sorting algorithm
        output = sort_fn(data)

        # Stop timer
        elapsed = time.perf_counter() - start

        # Verify correctness (important for testing)
        assert output == sorted(data)

        durations.append(elapsed)

    # Return average time across all trials
    return sum(durations) / len(durations)


def main():
    # Different input sizes to test scalability
    sizes = [1000, 2000, 4000, 8000]

    # Different input scenarios
    scenarios = {
        "Random": make_random_list,
        "Sorted": make_sorted_list,
        "Reverse Sorted": make_reverse_sorted_list,
        "Repeated Elements": make_repeated_list,
    }

    print("Average runtime in seconds")
    print("-" * 60)

    # Loop through each scenario
    for label, builder in scenarios.items():
        print(f"\nScenario: {label}")

        # Table header
        print(f"{'n':>8} {'Randomized':>15} {'Deterministic':>15}")

        # Test each input size
        for n in sizes:
            # Measure average runtime for both algorithms
            r_time = average_runtime(randomized_quicksort, builder, n)
            d_time = average_runtime(deterministic_quicksort, builder, n)

            # Print results in aligned format
            print(f"{n:>8} {r_time:>15.6f} {d_time:>15.6f}")

# Run when this script is executed directly
if __name__ == "__main__":
    main()