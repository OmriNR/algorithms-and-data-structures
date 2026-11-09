from DataSturctures.queue import Queue, sort_queue

def bucket_sort(arr):
    if len(arr) <= 1:
        return arr

    n = len(arr)

    buckets = [Queue() for _ in range(n)]

    for x in arr:
        b_idx = int(x * n)
        if b_idx >= n:
            b_idx = n - 1
        buckets[b_idx].enqueue(x)

    result = []
    for bucket in buckets:
        sorted_bucket = sort_queue(bucket)
        while not sorted_bucket.is_empty():
            result.append(sorted_bucket.dequeue())

    return result

def lsd_radix_sort(arr): #O(d * (n + 10))
    if not arr:
        return arr

    max_val = max(arr)

    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10

    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for num in arr:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    for i in range(n):
        arr[i] = output[i]

def msd_radix_sort(arr):
    if len(arr) <= 1:
        return arr

    max_val = max(arr)
    exp = 1

    while max_val // (exp * 10) > 0:
        exp *= 10

    def _msd_sort(sub_arr, current_exp):
        
        if len(sub_arr) <= 1 or current_exp == 0:
            return sub_arr

        buckets = [[] for _ in range(10)]
        for num in sub_arr:
            digit = (num // current_exp) % 10
            buckets[digit].append(num)

        result = []
        for bucket in buckets:
            sorted_bucket = _msd_sort(bucket, current_exp // 10)
            result.extend(sorted_bucket)

        return result
    
    return _msd_sort(arr, exp)