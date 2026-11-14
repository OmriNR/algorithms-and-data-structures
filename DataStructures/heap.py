# ---------- Array functions (work on a plain list, max-heap order) ----------

def heapify(arr, n, i):
    """Sift down arr[i] inside arr[0:n] so the subtree rooted at i is a max-heap. O(log n)"""
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest == i:
            break

        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def build_max_heap(arr):
    """Turn arr into a max-heap in place. O(n)"""
    n = len(arr)
    # Leaves are already heaps - start from the last parent and go up to the root.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    return arr


# ---------- Heap classes ----------

class _Heap:
    """Shared logic. Subclasses decide the order with _before(a, b)."""

    def __init__(self, arr=None):
        self.data = list(arr) if arr is not None else []
        self._build_heap()

    def _before(self, a, b) -> bool:
        """True if a should be above b in the heap."""
        raise NotImplementedError

    # index math
    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _sift_up(self, i: int) -> None:  # O(log n)
        while i > 0 and self._before(self.data[i], self.data[self._parent(i)]):
            parent = self._parent(i)
            self._swap(i, parent)
            i = parent

    def _sift_down(self, i: int) -> None:  # O(log n)
        n = len(self.data)
        while True:
            best = i
            left = self._left(i)
            right = self._right(i)

            if left < n and self._before(self.data[left], self.data[best]):
                best = left
            if right < n and self._before(self.data[right], self.data[best]):
                best = right

            if best == i:
                break

            self._swap(i, best)
            i = best

    def _build_heap(self) -> None:  # O(n)
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._sift_down(i)

    # public operations
    def is_empty(self) -> bool:  # O(1)
        return len(self.data) == 0

    def insert(self, x) -> None:  # O(log n)
        self.data.append(x)
        self._sift_up(len(self.data) - 1)

    def peek(self):  # O(1)
        if self.is_empty():
            raise IndexError("peek from an empty heap")
        return self.data[0]

    def extract(self):  # O(log n)
        if self.is_empty():
            raise IndexError("extract from an empty heap")

        root = self.data[0]
        last = self.data.pop()
        if self.data:  # if items are left, move the last one to the root and fix down
            self.data[0] = last
            self._sift_down(0)
        return root

    def delete_at(self, i: int):  # O(log n)
        """Remove and return the item at index i."""
        n = len(self.data)
        if i < 0 or i >= n:
            raise IndexError("heap index out of range")

        removed = self.data[i]
        last = self.data.pop()
        if i == n - 1:  # removed the last cell - nothing to fix
            return removed

        self.data[i] = last
        # The new value may break the rule upwards or downwards, only one can happen.
        if i > 0 and self._before(self.data[i], self.data[self._parent(i)]):
            self._sift_up(i)
        else:
            self._sift_down(i)
        return removed

    def index_of(self, x) -> int:  # O(n) - a heap is not sorted, so we scan
        for i in range(len(self.data)):
            if self.data[i] == x:
                return i
        return -1

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.data})"


class MinHeap(_Heap):
    """The root is the minimum (this is the heap rule from the lecture)."""

    def _before(self, a, b) -> bool:
        return a < b

    def extract_min(self):
        return self.extract()


class MaxHeap(_Heap):
    """The root is the maximum."""

    def _before(self, a, b) -> bool:
        return a > b

    def extract_max(self):
        return self.extract()
