from DataSturctures.binary_tree import TreeNode
from DataSturctures.stack import Stack


#Recursive and need to slice list, don't submit that
def bst_from_preorder_recursive(preorder: list[int]) -> TreeNode | None:
    if not preorder:
        return None

    root = TreeNode(preorder[0])

    split_idx = len(preorder)

    for i in range(1, len(preorder)):
        if preorder[i] > root.val:
            split_idx = i
            break

    root.left = bst_from_preorder_recursive(preorder[1:split_idx])
    root.right = bst_from_preorder_recursive(preorder[split_idx:])

    return root


#Using stack, submit that
def bst_from_preorder(preorder: list[int]) -> TreeNode | None:
    if not preorder:
        return None

    root = TreeNode(preorder[0])
    stack = Stack()
    stack.push(root)

    for index in range(1, len(preorder)):
        val = preorder[index]

        node = TreeNode(val)

        if val < stack.top().val:
            stack.top().left = node
        else:
            parent = stack.top()
            while not stack.is_empty() and stack.top().val < val:
                parent = stack.pop()
            parent.right = node

        stack.push(node)

    return root
