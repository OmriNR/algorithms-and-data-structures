class ArrayStack:
    def __init__(self, capacity: int = 1000):  # CREATE, O(1)
        self._data = [None] * capacity  # m cells allocated up front
        self._capacity = capacity       # m
        self._top = 0                   # i - number of items / next free cell

    def is_empty(self) -> bool:  # O(1)
        return self._top == 0

    def is_full(self) -> bool:  # O(1)
        return self._top == self._capacity

    def push(self, x) -> None:  # O(1)
        if self.is_full():
            raise OverflowError("Stack is full")
        self._data[self._top] = x
        self._top += 1

    def pop(self):  # O(1)
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        self._top -= 1
        x = self._data[self._top]
        self._data[self._top] = None
        return x

    def top(self):  # O(1) - look at the top without removing it
        if self.is_empty():
            raise IndexError("top from an empty stack")
        return self._data[self._top - 1]

    def empty(self) -> None:  # O(1) - just reset the index
        self._top = 0

    def __len__(self) -> int:
        return self._top

    def __repr__(self) -> str:
        items = ", ".join(repr(self._data[k]) for k in range(self._top))
        return f"ArrayStack([{items}] <- top)"


class _Node:
    def __init__(self, val, next_node=None):
        self.val = val
        self.next = next_node


class LinkedListStack:
    def __init__(self):  # CREATE, O(1)
        self._head = None  # T - the top of the stack
        self._size = 0

    def is_empty(self) -> bool:  # O(1)
        return self._head is None

    def push(self, x) -> None:  # O(1) - new node becomes the head
        self._head = _Node(x, self._head)
        self._size += 1

    def pop(self):  # O(1)
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        x = self._head.val
        self._head = self._head.next
        self._size -= 1
        return x

    def top(self):  # O(1)
        if self.is_empty():
            raise IndexError("top from an empty stack")
        return self._head.val

    def empty(self) -> None:  # O(n) - pop until empty, like in class
        while not self.is_empty():
            self.pop()

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = []
        node = self._head
        while node is not None:
            items.append(repr(node.val))
            node = node.next
        return f"LinkedListStack(top -> [{', '.join(items)}])"

Stack = LinkedListStack
