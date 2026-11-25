import random

def _next_prime(n : int) -> int:
    def is_prime(num : int) -> bool:
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    while not is_prime(n):
        n += 1
    return n

class ChaningHashTable:
    def __init__(self, initial_size: int = 7):
        self.size = _next_prime(initial_size)
        self.count = 0
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key) -> int:
        return hash(key) % self.size

    def _rehash(self):
        old_table = self.table
        self.size = _next_prime(self.size * 2)
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for bucket in old_table:
            for k, v in bucket:
                self.insert(k,v)

    def insert(self, key, value):
        if self.count / self.size > 0.75:
            self._rehash()

        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[idx].append([key, value])
        self.count += 1

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v

        raise KeyError(key)

    def delete(self, key):
        idx = self._hash(key)
        for i, (k, _) in enumerate(self.table[idx]):
            if k != key:
                continue
            self.table[idx].pop(i)
            self.count -= 1
            return
        raise KeyError(key)

    def __contains__(self, key) -> bool:
        idx = self._hash(key)
        return any(k == key for k, _ in self.table[idx])

    def __len__(self) -> int:
        return self.count

    def items(self):
        for bucket in self.table:
            for k, v in bucket:
                yield k, v

class OpenAddressingHashTable:
    _DELETED = object()

    def __init__(self, initial_size = 7, method: str = "linear"):
        if method not in ("linear", "quadratic", "double"):
            raise ValueError("method muse be linearm, quadratic or double")
        self.size = _next_prime(initial_size)
        self.method = method
        self.count = 0
        self.table = [None] * self.size

    def _hash11(self, key) -> int:
        return hash(key) % self.size

    def _hash2(self, key) -> int:
        return 1 + (hash(key) % (self.size -1))

    def _probe(self, key, i: int) -> int:
        h1 = self._hash11(key)
        if self.method == "linear":
            return (h1 + i) % self.size
        elif self.method == "quadratic":
            return (h1 + i * i) % self.size
        else:
            return (h1 + i * self._hash2(key)) % self.size

    def _rehash(self):
        old_table = self.table
        self.size = _next_prime(self.size * 2)
        self.table = [None] * self.size
        self.count = 0
        for item in old_table:
            if item is not None and item is not self._DELETED:
                self.insert(item[0], item[1])

    def insert(self, key, value):
        if (self.count + 1) / self.size > 0.5:
            self._rehash()

        first_deleted_idx = None
        for i in range(self.size):
            idx = self._probe(key, i)
            slot = self.table[idx]

            if slot is None:
                target = first_deleted_idx if first_deleted_idx is not None else idx
                self.table[target] = (key, value)
                self.count += 1
                return
            elif slot is self._DELETED:
                if first_deleted_idx is None:
                    first_deleted_idx = idx
            elif slot[0] == key:
                self.table[idx] = (key, value)
                return
        
        self._rehash()
        self.insert(key, value)

    def get(self, key):
        for i in range(self.size):
            idx = self._probe(key, i)
            slot = self.table[idx]
            if slot is None:
                break
            if slot is not self._DELETED and slot[0] == key:
                return slot[1]
        raise KeyError(key)

    def delete(self, key):
        for i in range(self.size):
            idx = self._probe(key, i)
            slot = self.table[idx]
            if slot is None:
                break
            if slot is not self._DELETED and slot[0] == key:
                self.table[idx] = self._DELETED
                self.count -= 1
                return
        raise KeyError(key)

    def __contains__(self, key) -> bool:
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        return self.count

    def items(self):
        for item in self.table:
            if item is not None and item is not self._DELETED:
                yield item[0], item[1]

class CuckooHashTable:
    def __init__(self, initial_size = 7):
        self.size = _next_prime(initial_size)
        self.t1 = [None] * self.size
        self.t2 = [None] * self.size
        self.count = 0
        self.salt1 = random.randint(1, 10**9)
        self.salt2 = random.randint(1, 10**9)

    def _h1(self, key) -> int:
        return hash((key, self.salt1)) % self.size

    def _h2(self, key) -> int:
            return hash((key, self.salt2)) % self.size

    def get(self, key):

        slot1 = self.t1[self._h1(key)]
        if slot1 is not None and slot1[0] == key:
            return slot1[1]

        slot2 = self.t2[self._h2(key)]
        if slot2 is not None and slot2[0] == key:
            return slot2[1]

        raise KeyError(key)

    def delete(self, key):

        idx1 = self._h1(key)
        if self.t1[idx1] is not None and self.t1[idx1][0] == key:
            self.t1[idx1] = None
            self.count -= 1
            return

        idx2 = self._h2(key)
        if self.t2[idx2] is not None and self.t2[idx2][0] == key:
            self.t2[idx2] = None
            self.count -= 1
            return

        raise KeyError(key)

    def __contains__(self, key) -> bool:
        slot1 = self.t1[self._h1(key)]
        if slot1 is not None and slot1[0] == key:
            return True
        slot2 = self.t2[self._h2(key)]
        return slot2 is not None and slot2[0] == key

    def __len__(self) -> int:
        return self.count

    def items(self):
        for slot in self.t1:
            if slot is not None:
                yield slot[0], slot[1]
        for slot in self.t2:
            if slot is not None:
                yield slot[0], slot[1]

    def _rehash(self, grow: bool = True):
        items = [x for x in self.t1 if x is not None] + [x for x in self.t2 if x is not None]
        if grow:
            self.size = _next_prime(self.size * 2)
        self.t1 = [None] * self.size
        self.t2 = [None] * self.size
        self.count = 0

        self.salt1 = random.randint(1, 10**9)
        self.salt2 = random.randint(1, 10**9)

        for k, v in items:
            self.insert(k, v)

    def insert(self, key, value):
        idx1 = self._h1(key)
        if self.t1[idx1] is not None and self.t1[idx1][0] == key:
            self.t1[idx1] = (key, value)
            return

        idx2 = self._h2(key)
        if self.t2[idx2] is not None and self.t2[idx2][0] == key:
            self.t2[idx2] = (key, value)
            return

        if (self.count + 1) / (2 * self.size) > 0.45:
            self._rehash(grow=True)

        item = (key, value)
        max_evictions = 2 * self.size

        for _ in range(max_evictions):
            idx1 = self._h1(item[0])
            self.t1[idx1], item = item, self.t1[idx1]
            if item is None:
                self.count += 1
                return

            idx2 = self._h2(item[0])
            self.t2[idx2], item = item, self.t2[idx2]
            if item is None:
                self.count += 1
                return

        self._rehash(grow=True)
        self.insert(item[0], item[1])

HashTable = CuckooHashTable