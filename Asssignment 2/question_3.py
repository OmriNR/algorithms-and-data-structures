class Node:
    def __init__(self,value):
        self.value = value
        self.next = None

def remove_duplicates(head: Node): #O(n^2)
    if head is None or head.next is None:
        return head

    current = head

    while current is not None:
        runner = current

        while runner.next is not None:
            if runner.next.value == current.value:
                runner.next = runner.next.next
            else:
                runner = runner.next

        current = current.next

    return head

def remove_duplicates(head: Node, m: int): #O(n)
    if head is None or head.next is None:
        return head

    seen = [False] * (m + 1)

    seen[head.value] = True
    current = head

    while current is not None:
        next_val = current.next.value

        if seen[next_val]:
            current.next = current.next.next
        else:
            seen[next_val] = True
            current = current.next
    
    return head