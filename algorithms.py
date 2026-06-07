import random


def randomized_quicksort(items):
    data = list(items)

    def sort_range(left, right):
        while left < right:
            pivot_pos = random.randint(left, right)
            pivot_value = data[pivot_pos]
            data[left], data[pivot_pos] = data[pivot_pos], data[left]

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

            if (less - left) < (right - greater):
                sort_range(left, less - 1)
                left = greater + 1
            else:
                sort_range(greater + 1, right)
                right = less - 1

    if len(data) <= 1:
        return data

    sort_range(0, len(data) - 1)
    return data


def deterministic_quicksort(items):
    data = list(items)

    def sort_range(left, right):
        while left < right:
            pivot_value = data[left]

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

            if (less - left) < (right - greater):
                sort_range(left, less - 1)
                left = greater + 1
            else:
                sort_range(greater + 1, right)
                right = less - 1

    if len(data) <= 1:
        return data

    sort_range(0, len(data) - 1)
    return data


class ChainNode:
    def __init__(self, key, value, nxt=None):
        self.key = key
        self.value = value
        self.next = nxt


class ChainingHashTable:
    def __init__(self, capacity=11, max_load=0.75):
        self.capacity = max(5, capacity)
        self.table = [None] * self.capacity
        self.size = 0
        self.max_load = max_load

        self.prime = 109345121
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

    def _base_hash(self, key):
        return hash(key) & 0x7FFFFFFF

    def _index(self, key):
        raw = self._base_hash(key)
        return ((self.a * raw + self.b) % self.prime) % self.capacity

    def load_factor(self):
        return self.size / self.capacity

    def insert(self, key, value):
        idx = self._index(key)
        current = self.table[idx]

        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        self.table[idx] = ChainNode(key, value, self.table[idx])
        self.size += 1

        if self.load_factor() > self.max_load:
            self._resize(self.capacity * 2 + 1)

    def search(self, key):
        idx = self._index(key)
        current = self.table[idx]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def delete(self, key):
        idx = self._index(key)
        current = self.table[idx]
        previous = None

        while current:
            if current.key == key:
                if previous is None:
                    self.table[idx] = current.next
                else:
                    previous.next = current.next
                self.size -= 1
                return True
            previous = current
            current = current.next

        return False

    def _resize(self, new_capacity):
        old_pairs = []

        for head in self.table:
            current = head
            while current:
                old_pairs.append((current.key, current.value))
                current = current.next

        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.size = 0
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

        for key, value in old_pairs:
            self.insert(key, value)

