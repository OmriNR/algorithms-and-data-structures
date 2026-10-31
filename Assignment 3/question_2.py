class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def print_part_sorted(node: TreeNode, x, y):
    if node is None:
        return

    if node.val >= y:
        print_part_sorted(node.left, x, y)
    
    elif node.val <= x:
        print_part_sorted(node.right, x, y)

    else:
        print_part_sorted(node.left, x, y)
        print(f"next value: {node.val}")
        print_part_sorted(node.right, x, y)


    