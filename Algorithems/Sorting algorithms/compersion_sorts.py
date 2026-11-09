from DataSturctures.heap import heapify

def selection_sort(arr): #O(n^2)
    n = len(arr)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

def insertion_sort(arr): #O(n^2), O(n) if already sorted
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i-1

        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

def bubble_sort(arr): #O(n^2), O(n) if already sorted
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i -1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr

def heap_sort(arr): #O(nlogn)
    n = len(arr)

    for i in range( n // 2 -1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr

def quick_sort(arr, low = 0, high = None): #O(logn)
    if high is None:
        high = len(arr) - 1

    if low < high:
        p_idx = partition(arr, low, high)

        quick_sort(arr, low, p_idx -1)
        quick_sort(arr, p_idx + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i+1

def merge_sort(arr): #O(nlogn)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result