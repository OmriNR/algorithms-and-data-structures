def heapify_down(heap, i):
    n = len(heap)

    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and heap[left] > heap[largest]:
            largest = left
        if right < n and heap[right] > heap[largest]:
            largest = right

        if largest == i:
            break

        heap[i], heap[largest] = heap[largest], heap[i]
        i = largest

def heapify_up(heap, i):
    while i > 0:
        parent = (i-1) // 2
        if heap[i] > heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break

def delete_val(heap, x):
    target_index = -1
    for i in range(heap):
        if heap[i] == x:
            target_index = i
            break

def delete_by_index(heap, i):
    n = len(heap)
    if i < 0 or i >= n:
        return

    if i == n - 1:
        return

    old_val = heap[i]

    heap[i] = heap.pop()
    new_val = heap[i]

    if new_val > old_val:
        heapify_up(heap, i)
    else:
        heapify_down(heap, i)