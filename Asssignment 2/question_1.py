class MinStack:
    def __init__(self):
        self.stack = []
    

    def push(self ,x):
        self.stack.append(x)

    def pop(self):
        if len(self.stack) == 0:
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def min(self):
        if self.is_empty():
            return -1

        help_stack = MinStack()
            
        min_val = self.stack.pop()
        help_stack.push(min_val)

        while not self.is_empty():
            x = self.stack.pop()
            help_stack.append(x)

            if x < min_val:
                min_val = x
            
        while not help_stack.is_empty():
            self.stack.append(help_stack.pop())

        return min_val
            
class MinStackEfficient:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x):
        self.stack.append(x)

        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self):
        if not self.stack:
            raise IndexError("Stack is empty")

        x = self.stack.pop()

        if x == self.min_stack[-1]:
            self.min_stack.pop()

    def min(self):
        if not self.min_stack:
            return -1

        return self.min_stack[-1]