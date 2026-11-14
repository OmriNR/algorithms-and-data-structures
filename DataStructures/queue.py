class ArrayQueue:
    def __init__(self, capacity: int = 1000):  # CREATE, O(1)
        self._data = [None] * capacity  # A, m cells
        self._capacity = capacity       # m
        self._in = 0                    # where the next item is written
        self._out = 0                   # where the next item is read
        self._size = 0                  # s

    def is_empty(self) -> bool:  # O(1)
        return self._size == 0

    def is_full(self) -> bool:  # O(1)
        return self._size == self._capacity

    def enqueue(self, x) -> None:  # O(1)
        if self.is_full():
            raise OverflowError("Queue is full")
        self._data[self._in] = x
        self._in = (self._in + 1) % self._capacity  # wrap around
        self._size += 1

    def dequeue(self):  # O(1)
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        x = self._data[self._out]
        self._data[self._out] = None
        self._out = (self._out + 1) % self._capacity  # wrap around
        self._size -= 1
        return x

    def front(self):  # O(1) - look at the front without removing it
        if self.is_empty():
            raise IndexError("front from an empty queue")
        return self._data[self._out]

    def empty(self) -> None:  # O(1)
        self._in = self._out = self._size = 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = ", ".join(
            repr(self._data[(self._out + k) % self._capacity]) for k in range(self._size)
        )
        return f"ArrayQueue(front -> [{items}] <- back)"


class _Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedListQueue:
    def __init__(self):  # CREATE, O(1)
        self._out = None  # head of the list - front of the queue
        self._in = None   # tail of the list - back of the queue
        self._size = 0

    def is_empty(self) -> bool:  # O(1)
        return self._out is None

    def enqueue(self, x) -> None:  # O(1)
        node = _Node(x)
        if self.is_empty():
            self._in = self._out = node
        else:
            self._in.next = node
            self._in = node
        self._size += 1

    def dequeue(self):  # O(1)
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        x = self._out.val
        self._out = self._out.next
        if self._out is None:  # queue became empty
            self._in = None
        self._size -= 1
        return x

    def front(self):  # O(1)
        if self.is_empty():
            raise IndexError("front from an empty queue")
        return self._out.val

    def empty(self) -> None:  # O(n) - dequeue until empty, like in class
        while not self.is_empty():
            self.dequeue()

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = []
        node = self._out
        while node is not None:
            items.append(repr(node.val))
            node = node.next
        return f"LinkedListQueue(front -> [{', '.join(items)}] <- back)"

def sort_queue(q: Queue) -> Queue:
    sorted_q = Queue()

    while not q.is_empty():
        val = q.dequeue()
        k = sorted_q.size()
        inserted = False

        for _ in range(k):
            curr = sorted_q.dequeue()
            if not inserted and val <= curr:
                sorted_q.enqueue(val)
                inserted = True
            sorted_q.enqueue(curr)

        if not inserted:
            sorted_q.enqueue(val)

    return sorted_q
# Default queue: the linked list version has no size limit.
Queue = LinkedListQueue
