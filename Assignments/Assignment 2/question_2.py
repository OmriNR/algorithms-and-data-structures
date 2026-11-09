from DataSturctures.queue import Queue
from DataSturctures.stack import Stack


def flip_part(queue: Queue, k: int) -> Queue:  # O(n)
    queue_length = len(queue)
    stack = Stack()

    for i in range(k):
        stack.push(queue.dequeue())

    for i in range(k):
        queue.enqueue(stack.pop())

    for i in range(queue_length - k):
        queue.enqueue(queue.dequeue())

    return queue
