# Understanding Algorithm Efficiency and Scalability: Randomized Quicksort and Hashing With Chaining

## Introduction

One of the main reasons algorithm analysis matters is that two correct solutions can behave very differently when the input becomes large or structured in an unfavorable way. In other words, correctness alone is not enough. A good algorithm should also remain efficient as the problem scales.

This assignment focuses on two important algorithmic ideas. The first is Quicksort, a widely used divide-and-conquer sorting algorithm. Although Quicksort is often fast in practice, its performance depends heavily on how the pivot is chosen. A poor pivot rule can cause serious slowdowns. Randomization improves Quicksort by making bad pivot patterns much less likely. Previous studies of Randomized Quicksort show that its expected number of comparisons is **O(n log n)**, which explains why it remains efficient on average even though individual runs may vary (Acharya, n.d.; Sryheni, 2024).

The second topic is hashing with chaining. Hashing supports efficient retrieval by mapping keys into slots of a table. Because collisions are unavoidable, a way to handle them is needed. Chaining is a common approach where each slot stores a linked list of all values that map to that slot. Under simple uniform hashing, the expected running time of insert, search, and delete operations depends on the load factor (**α = n/m**), where *n* is the number of elements and *m* is the number of slots (Cormen et al., 2001; GeeksforGeeks, 2025a).

Together, these topics show how theory and real implementation come together when analyzing algorithm efficiency.

---

## Part 1: Randomized Quicksort

### Implementation

I implemented Randomized Quicksort so that the pivot is chosen randomly from the current subarray in every recursive call. This avoids the weakness of always picking a fixed position like the first element.

To make the implementation more effective, I used three-way partitioning. Instead of splitting into just two parts, the algorithm separates elements into:

- values less than the pivot 
- values equal to the pivot 
- values greater than the pivot 

This approach works better when there are duplicate values because it avoids unnecessary recursive calls on equal elements.

The implementation correctly handles several edge cases such as:

- empty arrays 
- single-element arrays 
- already sorted arrays 
- reverse-sorted arrays 
- arrays with repeated values 

---

### Average-Case Analysis

A more precise way to analyze Randomized Quicksort is by looking at the expected number of comparisons.

Assume the input elements are sorted as:

z₁, z₂, …, zₙ


For each pair *(i, j)* where *i < j*, define an indicator variable:

Xᵢⱼ = 1 if zᵢ and zⱼ are compared
Xᵢⱼ = 0 otherwise


The total number of comparisons is:

X = Σ Xᵢⱼ


Two elements are compared only if one of them is chosen as the first pivot among:

{zᵢ, zᵢ₊₁, …, zⱼ}


Because the pivot is selected randomly:

P(Xᵢⱼ = 1) = 2 / (j − i + 1)


Using linearity of expectation:

E[X] = Σ P(Xᵢⱼ = 1)


This simplifies to a harmonic series, resulting in:

E[X] = O(n log n)


So, the expected running time of Randomized Quicksort is:

**O(n log n)**

---

### Deterministic Quicksort Comparison

For comparison, I also implemented deterministic Quicksort using the first element as the pivot.

In this case, the recurrence becomes:

T(n) = T(n − 1) + Θ(n)


which solves to:

Θ(n²)


This happens when the pivot repeatedly ends up being the smallest or largest element, causing very unbalanced partitions.

---

### Empirical Comparison

I compared the two algorithms using:

1. Random arrays  
2. Already sorted arrays  
3. Reverse-sorted arrays  
4. Arrays with repeated elements  

#### Observed Trends

- On **random arrays**, both algorithms performed similarly  
- On **sorted and reverse-sorted arrays**, deterministic Quicksort slowed down significantly  
- **Randomized Quicksort remained stable** across all inputs  
- On **arrays with repeated values**, performance improved due to three-way partitioning  

---

## Part 2: Hashing With Chaining

### Implementation

In this part, I implemented a hash table using chaining.

- The table is an array of slots  
- Each slot contains a linked list  
- Collisions are handled by storing multiple values in the same list  

Supported operations:

- **Insert** – add or update key-value pair  
- **Search** – retrieve value  
- **Delete** – remove key-value pair  

The hash function used:

h(k) = ((a · hash(k) + b) mod p) mod m


Where:

- *p* is a large prime  
- *a* and *b* are random constants  
- *m* is the table size  

Dynamic resizing is used when the table becomes too full.

---

### Expected-Time Analysis

Under simple uniform hashing:

- Each key is equally likely to map to any slot  

Let:

- *n* = number of elements  
- *m* = number of slots  
- *α = n/m* (load factor)  

Expected runtimes:

- Unsuccessful search → **O(1 + α)**  
- Successful search → **O(1 + α)**  
- Insert → **O(1 + α)**  
- Delete → **O(1 + α)**  

---

### Effect of Load Factor

If **α is small**:

- chains are short  
- collisions are fewer  
- operations are faster  

If **α is large**:

- chains grow longer  
- more comparisons are needed  
- performance decreases  

Resizing helps maintain efficiency by reducing α.

---

### Reducing Collisions

Common strategies:

1. Use a better hash function  
2. Resize dynamically  
3. Maintain a low load factor  
4. Use efficient chaining structures  

---

## Conclusion

This assignment showed that algorithm performance is not just about correctness, but also about how the algorithm behaves under different input conditions.

Randomized Quicksort improves stability by reducing the chances of bad pivot selection, keeping its expected runtime at **O(n log n)**. Deterministic Quicksort, on the other hand, can degrade to **O(n²)** on structured inputs.

Hashing with chaining demonstrates how performance can remain efficient as long as collisions are controlled and the load factor is managed.

Overall, this assignment helped connect theoretical analysis with real-world implementation.

---

## References

- Acharya, M. (n.d.). *Expected number of comparisons in randomized quicksort*  
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2001). *Introduction to algorithms*  
- GeeksforGeeks. (2025a). *Separate chaining collision handling technique in hashing*  
- GeeksforGeeks. (2025b). *When does the worst case of quicksort occur?*  
- GeeksforGeeks. (2026). *Load factor and rehashing*  
- Sryheni, S. (2024). *Understanding randomized quicksort*, Baeldung