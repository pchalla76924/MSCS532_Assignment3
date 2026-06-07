import random


def randomized_quicksort(items):
    # Create a copy so original input is not modified
    data = list(items)

    def sort_range(left, right):
        # Continue sorting while there are elements
        while left < right:

            # Pick a random pivot index inside current range
            pivot_pos = random.randint(left, right)
            pivot_value = data[pivot_pos]

            # Move the pivot to the beginning
            data[left], data[pivot_pos] = data[pivot_pos], data[left]

            # Initialize pointers for 3-way partitioning
            less = left          # elements < pivot
            scan = left + 1      # current scanning index
            greater = right      # elements > pivot

            # Partition array into three parts
            while scan <= greater:
                if data[scan] < pivot_value:
                    # Move element to "less than pivot" section
                    data[less], data[scan] = data[scan], data[less]
                    less += 1
                    scan += 1
                elif data[scan] > pivot_value:
                    # Move element to "greater than pivot" section
                    data[scan], data[greater] = data[greater], data[scan]
                    greater -= 1
                else:
                    # Element equals pivot → just move forward
                    scan += 1

            # Optimization: sort smaller partition first
            # to reduce recursion depth
            if (less - left) < (right - greater):
                sort_range(left, less - 1)
                left = greater + 1
            else:
                sort_range(greater + 1, right)
                right = less - 1

    # Edge case: empty or single element list
    if len(data) <= 1:
        return data

    # Start sorting entire array
    sort_range(0, len(data) - 1)
    return data


def deterministic_quicksort(items):
    # Copy input list
    data = list(items)

    def sort_range(left, right):
        while left < right:

            # Always pick the first element as pivot
            pivot_value = data[left]

            # Same partitioning logic as randomized version
            less = left
            scan = left + 1
            greater = right

            while scan <= greater:
                if data[scan] < pivot_value:
                    data[less], data[scan] = data[scan], data[less]
                    less += 1
                    scan += 1
                elif data[scan] > pivot_value:
                    data[scan], data[greater] = data[greater], data[scan]
                    greater -= 1
                else:
                    scan += 1

            # Same tail-recursive optimization
            if (less - left) < (right - greater):
                sort_range(left, less - 1)
                left = greater + 1
            else:
                sort_range(greater + 1, right)
                right = less - 1

    # Handle simple cases
    if len(data) <= 1:
        return data

    sort_range(0, len(data) - 1)
    return data


# Node class used in the linked list for each bucket
class ChainNode:
    def __init__(self, key, value, nxt=None):
        self.key = key
        self.value = value
        self.next = nxt


class ChainingHashTable:
    def __init__(self, capacity=11, max_load=0.75):
        # Initialize table size and load factor threshold
        self.capacity = max(5, capacity)
        self.table = [None] * self.capacity
        self.size = 0
        self.max_load = max_load

        # Parameters for universal hashing function
        self.prime = 109345121
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

    def _base_hash(self, key):
        # Ensure non-negative hash value
        return hash(key) & 0x7FFFFFFF

    def _index(self, key):
        # Universal hashing formula to reduce collisions
        raw = self._base_hash(key)
        return ((self.a * raw + self.b) % self.prime) % self.capacity

    def load_factor(self):
        # Returns current load factor α = size / capacity
        return self.size / self.capacity

    def insert(self, key, value):
        idx = self._index(key)
        current = self.table[idx]

        # Check if key already exists → update value
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Insert new node at beginning of chain
        self.table[idx] = ChainNode(key, value, self.table[idx])
        self.size += 1

        # Resize table if load factor becomes too large
        if self.load_factor() > self.max_load:
            self._resize(self.capacity * 2 + 1)

    def search(self, key):
        idx = self._index(key)
        current = self.table[idx]

        # Traverse chain to find key
        while current:
            if current.key == key:
                return current.value
            current = current.next

        # Key not found
        return None

    def delete(self, key):
        idx = self._index(key)
        current = self.table[idx]
        previous = None

        # Traverse chain to locate key
        while current:
            if current.key == key:
                # Remove node from linked list
                if previous is None:
                    self.table[idx] = current.next
                else:
                    previous.next = current.next

                self.size -= 1
                return True

            previous = current
            current = current.next

        return False  # Key not found

    def _resize(self, new_capacity):
        # Store all existing key-value pairs
        old_pairs = []

        for head in self.table:
            current = head
            while current:
                old_pairs.append((current.key, current.value))
                current = current.next

        # Create new larger table
        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.size = 0

        # Generate new hashing parameters
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

        # Reinsert old elements into new table
        for key, value in old_pairs:
            self.insert(key, value)

