from DataSturctures.stack import Stack


class MinStack:
    def __init__(self):
        self.stack = Stack()

    def push(self, x):
        self.stack.push(x)

    def pop(self):
        if self.stack.is_empty():
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def is_empty(self):
        return self.stack.is_empty()

    def min(self):  # O(n) - empty into a helper stack while tracking the min, then restore
        if self.is_empty():
            return -1

        help_stack = Stack()

        min_val = self.stack.pop()
        help_stack.push(min_val)

        while not self.stack.is_empty():
            x = self.stack.pop()
            help_stack.push(x)

            if x < min_val:
                min_val = x

        while not help_stack.is_empty():
            self.stack.push(help_stack.pop())

        return min_val


class MinStackEfficient:
    def __init__(self):
        self.stack = Stack()
        self.min_stack = Stack()  # top is always the current minimum

    def push(self, x):  # O(1)
        self.stack.push(x)

        if self.min_stack.is_empty() or x <= self.min_stack.top():
            self.min_stack.push(x)

    def pop(self):  # O(1)
        if self.stack.is_empty():
            raise IndexError("Stack is empty")

        x = self.stack.pop()

        if x == self.min_stack.top():
            self.min_stack.pop()

        return x

    def min(self):  # O(1)
        if self.min_stack.is_empty():
            return -1

        return self.min_stack.top()
