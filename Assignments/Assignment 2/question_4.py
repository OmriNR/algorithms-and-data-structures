from DataSturctures.heap import MaxHeap


def delete_by_index(heap: MaxHeap, i: int):  # O(log n)
    """
    Replace heap[i] with the last item and remove the last cell.
    If the new value is bigger than the old one it can only break the rule upwards (sift up),
    otherwise it can only break it downwards (sift down).
    """
    n = len(heap)
    if i < 0 or i >= n:
        return None

    old_val = heap.data[i]

    if i == n - 1:
        return heap.data.pop()

    heap.data[i] = heap.data.pop()
    new_val = heap.data[i]

    if new_val > old_val:
        heap._sift_up(i)
    else:
        heap._sift_down(i)

    return old_val


def delete_val(heap: MaxHeap, x):  # O(n) to find x + O(log n) to delete
    target_index = heap.index_of(x)
    if target_index == -1:
        return None
    return delete_by_index(heap, target_index)
