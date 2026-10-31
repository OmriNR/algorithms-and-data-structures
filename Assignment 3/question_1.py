class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def head(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

#Recursive and need to slice list, don't submit that
def bst_from_preorder(perorder: list[int]) -> TreeNode | None:
    if not preorder:
        return None

    root = TreeNode(perorder[0])

    split_idx = len(preorder)

    for i in range(1, len(preorder)):
        if perorder[i] > root.val:
            split_idx = i
            break
    
    root.left = bst_from_preorder(perorder[1:split_idx])
    root.right = bst_from_preorder(preorder[split_idx:])

    return root

#Using stack, submit that
def bst_from_preorder(preorder: list[int]) -> TreeNode | None:
    if not preorder:
        return None

    root = TreeNode(preorder[0])
    stack = Stack()
    stack.push(root)

    for index in range(1, n):
        val = preorder[index]
        
        node = TreeNode(val)

        if val < stack.head().val:
            stack.head().left = node
        else:
            parent = stack.head()
            while not stack.is_empty() and stack.head().val < val:
                parent = stack.pop()
            parent.right = node

        stack.push(node)
    
    return root