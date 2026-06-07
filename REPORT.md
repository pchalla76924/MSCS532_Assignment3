# Understanding Algorithm Efficiency and Scalability: Randomized Quicksort and Hashing With Chaining


## Introduction

One of the main reasons algorithm analysis matters is that two correct solutions can behave very differently when the input becomes large or structured in an unfavorable way. In other words, correctness alone is not enough. A good algorithm should also remain efficient as the problem scales.

This assignment focuses on two common algorithmic ideas. The first is Quicksort, a widely used divide-and-conquer sorting algorithm. Although Quicksort is often fast in practice, its performance depends heavily on pivot selection. A poor pivot rule can cause serious slowdowns. Randomization improves Quicksort by making bad pivot patterns much less likely. Analyses of Randomized Quicksort show that its expected number of comparisons is \(O(n \log n)\), which explains why it remains efficient on average even though individual runs may vary.

The second topic is hashing with chaining. Hashing supports efficient retrieval by mapping keys into slots of a table. Because collisions are unavoidable, a collision-resolution strategy is needed. Chaining is a standard method in which each slot stores a linked list of all items that hash there. Under simple uniform hashing, the expected running time of insert, search, and delete operations depends on the load factor \( \alpha = n/m \), where \(n\) is the number of elements and \(m\) is the number of slots.

Together, these two topics show how theoretical analysis and practical performance connect.

---

# Part 1: Randomized Quicksort

## Implementation

I implemented Randomized Quicksort so that the pivot is chosen uniformly at random from the current subarray in every recursive call. This follows the requirement from the assignment and avoids the weakness of using a fixed pivot rule.

I used a three-way partitioning strategy. Instead of dividing values only into “less than pivot” and “greater than pivot,” the algorithm creates three groups:

- values less than the pivot
- values equal to the pivot
- values greater than the pivot

This choice helps the implementation handle repeated values more efficiently. It also makes the algorithm more stable on inputs with many duplicates.

The implementation correctly handles edge cases such as:

- empty arrays
- single-element arrays
- already sorted arrays
- reverse-sorted arrays
- arrays containing repeated elements

---

## Average-Case Analysis

A rigorous way to analyze Randomized Quicksort is to count the expected number of comparisons.

Let the input elements be written in sorted order as:

\[
z_1, z_2, \dots, z_n
\]

For each pair \((i,j)\) with \(i < j\), define an indicator random variable:

\[
X_{ij} =
\begin{cases}
1, & \text{if } z_i \text{ and } z_j \text{ are compared} \\
0, & \text{otherwise}
\end{cases}
\]

The total number of comparisons made by the algorithm is then:

\[
X = \sum_{1 \le i < j \le n} X_{ij}
\]

The key observation is that two elements \(z_i\) and \(z_j\) are compared only if one of them is the first pivot chosen from the set:

\[
\{z_i, z_{i+1}, \dots, z_j\}
\]

If any element between them is selected as the first pivot, then the partition step separates the pair into different recursive subproblems, and they will never be compared later.

Since the pivot is chosen uniformly at random, the probability that either endpoint \(z_i\) or \(z_j\) is selected first from that set is:

\[
P(X_{ij}=1)=\frac{2}{j-i+1}
\]

Now apply linearity of expectation:

\[
E[X] = E\left[\sum_{1 \le i < j \le n} X_{ij}\right]
\]

\[
= \sum_{1 \le i < j \le n} E[X_{ij}]
\]

\[
= \sum_{1 \le i < j \le n} P(X_{ij}=1)
\]

\[
= \sum_{1 \le i < j \le n} \frac{2}{j-i+1}
\]

This sum is bounded by a harmonic-series expression and simplifies to:

\[
E[X] = O(n \log n)
\]

Because the running time of Quicksort is proportional to its comparisons and partitioning work, the expected running time of Randomized Quicksort is:

\[
O(n \log n)
\]

This is the main reason Randomized Quicksort is considered more reliable than fixed-pivot Quicksort for general use.

---

## Deterministic Quicksort Comparison

For comparison, I also implemented deterministic Quicksort using the first element as the pivot.

That version can behave poorly on already sorted or reverse-sorted inputs. If the first element is always the smallest or largest item, the partitions become extremely unbalanced. Instead of splitting the problem into two smaller pieces of similar size, the algorithm produces one empty side and one subarray of size \(n-1\).

That gives the recurrence:

\[
T(n)=T(n-1)+\Θ(n)
\]

which solves to:

\[
\Θ(n^2)
\]

So even though deterministic first-pivot Quicksort may look fine on random input, it becomes unreliable on structured inputs.

---

## Empirical Comparison

I compared Randomized Quicksort and deterministic first-pivot Quicksort on the following kinds of arrays:

1. randomly generated arrays 
2. already sorted arrays 
3. reverse-sorted arrays 
4. arrays with repeated elements 

The benchmark script in this repository measures average runtime across multiple trials.

### Observed Trends

The empirical results matched the theoretical expectations in a clear way:

- On **random arrays**, both algorithms performed reasonably well. 
- On **sorted** and **reverse-sorted arrays**, deterministic Quicksort slowed down much more noticeably as input size increased. 
- Randomized Quicksort remained more stable across all categories. 
- On **arrays with repeated elements**, both algorithms improved because the three-way partitioning approach grouped equal values efficiently.

One detail worth noting is that deterministic Quicksort can sometimes appear slightly faster on small random inputs because it avoids the overhead of selecting random pivots. However, that small constant-factor difference does not change the bigger picture. Randomized Quicksort is more robust when the input structure is unfavorable.

---

# Part 2: Hashing With Chaining

## Implementation

The second part of the assignment required implementing a hash table using chaining.

In this design, the hash table is an array of slots. Each slot stores the head of a linked list containing all key-value pairs that map to that index. When two keys hash to the same slot, the collision is resolved by storing both elements in the same chain.

The implementation supports the required operations:

- **Insert** – add or update a key-value pair 
- **Search** – retrieve the value for a given key 
- **Delete** – remove a key-value pair 

To reduce predictable collision patterns, I used a modular arithmetic compression method:

\[
h(k)=((a \cdot \text{hash}(k)+b)\bmod p)\bmod m
\]

where:

- \(p\) is a large prime
- \(a\) and \(b\) are randomly selected constants
- \(m\) is the current table size

I also included **dynamic resizing**. When the load factor becomes too large, the table expands and all existing key-value pairs are rehashed into the larger table.

---

## Expected-Time Analysis Under Simple Uniform Hashing

The usual assumption for analyzing hashing is **simple uniform hashing**. This means each key is equally likely to hash to any slot, independently of the others.

If the table contains \(n\) elements and has \(m\) slots, then the load factor is:

\[
\alpha = \frac{n}{m}
\]

This value represents the average number of elements stored per slot.

Because separate chaining stores collisions in linked lists, the expected length of a chain is approximately \( \alpha \). Therefore, the expected running times become:

- **Unsuccessful search:** \(O(1+\alpha)\)
- **Successful search:** \(O(1+\alpha)\)
- **Insert:** \(O(1+\alpha)\)
- **Delete:** \(O(1+\alpha)\)

The reason for the extra \(+\alpha\) term is simple: after computing the hash index in constant time, the algorithm may still need to walk through a chain of expected length \( \alpha \).

In the worst case, if many keys collide into one slot, the chain could grow to length \(n\), making operations \(O(n)\). However, under simple uniform hashing and with proper load-factor control, expected performance remains efficient.

---

## Effect of the Load Factor

The load factor has a direct effect on performance.

If \( \alpha \) is small:

- chains are short
- collisions are less frequent
- insert, search, and delete stay fast

If \( \alpha \) becomes large:

- chains become longer
- more comparisons are needed inside each chain
- operation time increases

This is why resizing matters. A good hash table should not keep growing indefinitely without increasing its number of slots. Once the table becomes too full, performance gradually weakens.

In this implementation, resizing occurs when the load factor exceeds a threshold. This keeps the average chain length under control and helps preserve expected-time efficiency.

---

## Strategies for Reducing Collisions

There are several ways to reduce the performance cost of collisions:

1. **Use a better hash compression method** 
   A more carefully designed hash function can spread keys more evenly.

2. **Resize the table dynamically** 
   Increasing the number of slots reduces the average chain length.

3. **Maintain a reasonable load factor** 
   Keeping \( \alpha \) low is one of the simplest and most effective ways to maintain good performance.

4. **Choose a suitable data structure for each chain** 
   In this assignment, linked lists are used because they are straightforward and fit well with chaining.

---

# Conclusion

This assignment showed that algorithm efficiency depends on both theory and implementation.

Randomized Quicksort remains efficient on average because random pivot selection prevents the same bad split pattern from repeating consistently. The indicator-variable analysis provides a rigorous reason for why the expected running time is \(O(n \log n)\). In contrast, deterministic first-pivot Quicksort can degrade to \( \	Θ(n^2) \) on sorted or reverse-sorted input.

Hashing with chaining illustrates a different side of algorithm analysis. Under simple uniform hashing, insert, search, and delete remain efficient in expectation, but that result depends on controlling collisions and keeping the load factor from growing too large.

The biggest lesson from this assignment is that performance guarantees are not just abstract formulas. They depend on assumptions, input structure, and implementation choices. That is what makes algorithm analysis useful in practice.

---

# References

Acharya, M. (n.d.). *Expected number of comparisons in randomized quicksort*. [PDF](https://acharyamanish.net/expository-notes/comparison-random-quicksort.pdf)

Bagchi, A. (2025, July 27). *Running time analysis for randomized quicksort*. [PDF](https://www.cse.iitd.ac.in/~bagchi/courses/COL863_25-26/randomized-quicksort-analysis-july-2025v2.pdf)

Baeldung. (2024, March 18). *Quick sort worst case time complexity*. [Article](https://www.baeldung.com/cs/quicksort-time-complexity-worst-case)

Duke University. (n.d.). *Hash tables*. [PDF](https://users.cs.duke.edu/~reif/courses/alglectures/upfal.lectures/hash.pdf)

Programming.Guide. (n.d.). *Hash tables: Complexity*. [Article](https://programming.guide/hash-tables-complexity.html)

University of Iowa. (2019, October 22). *Randomized quicksort* (CS:5350 lecture notes). [PDF](https://homepage.cs.uiowa.edu/~sriram/5350/fall19/notes/10.22/10.22.pdf)
