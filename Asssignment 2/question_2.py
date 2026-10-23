def flip_part(queue, k):
    queue_length = len(queue)
    stack = []

    for i in range(k):
        stack.append(queue.dequeue())
    
    for i in range(k):
        queue.enqueue(stack.pop())
    
    for i in range(queue_length -k):
        queue.enqueue(queue.dequeue())

    return queue