# This file is used to test all functions from algorithms.py
# using static (fixed) inputs instead of random benchmarks.
import sys
sys.tracebacklimit = 0  # Limit traceback to only the error message for cleaner output

from algorithms import (
    randomized_quicksort,
    deterministic_quicksort,
    ChainingHashTable
)


def test_quicksorts():
    print("=" * 60)
    print("Testing Quicksort Implementations")
    print("=" * 60)

    # Static test cases
    test_cases = [
        [],                         # empty list
        [5],                        # single element
        [4, 2, 6, 1, 3],            # random case
        [1, 2, 3, 4, 5],            # already sorted
        [5, 4, 3, 2, 1],            # reverse sorted
        [3, 3, 3, 2, 2, 1, 1],      # duplicates
        [10, -1, 7, 3, 0, -5]       # mixed positive/negative
    ]

    for i, case in enumerate(test_cases, start=1):
        expected = sorted(case)

        rand_sorted = randomized_quicksort(case)
        det_sorted = deterministic_quicksort(case)

        print(f"\nTest Case {i}: {case}")
        print(f"Expected      : {expected}")
        print(f"Randomized QS : {rand_sorted}")
        print(f"Deterministic : {det_sorted}")

        # Verify correctness
        assert rand_sorted == expected, "Randomized Quicksort failed!"
        assert det_sorted == expected, "Deterministic Quicksort failed!"

    print("\n All quicksort tests passed!")


def test_hash_table():
    print("\n" + "=" * 60)
    print("Testing Hash Table (Chaining)")
    print("=" * 60)

    table = ChainingHashTable()

    print("\n--- Insert operations ---")
    table.insert("apple", 10)
    table.insert("banana", 20)
    table.insert("orange", 30)

    # Insert duplicate key to test update
    table.insert("apple", 15)

    print("\n--- Search operations ---")
    print("apple ->", table.search("apple"))   # should be 15
    print("banana ->", table.search("banana"))
    print("grape ->", table.search("grape"))   # should be None

    assert table.search("apple") == 15
    assert table.search("banana") == 20
    assert table.search("grape") is None

    print("\n--- Delete operations ---")
    print("Deleting banana:", table.delete("banana"))
    print("Deleting mango:", table.delete("mango"))  # doesn't exist

    assert table.delete("apple") == True
    assert table.search("apple") is None

    print("\n Hash table tests passed!")


if __name__ == "__main__":
    test_quicksorts()
    test_hash_table()
