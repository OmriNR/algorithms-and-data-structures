from DataSturctures.queue import Queue


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"TreeNode({self.val!r})"


class BinaryTree:
    def __init__(self, root: TreeNode | None = None):  # CREATE, O(1)
        self.root = root

    def is_empty(self) -> bool:  # O(1)
        return self.root is None

    def inorder(self) -> list:
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.val)
        self._inorder(node.right, result)

    def preorder(self) -> list:
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result) -> None:
        if node is None:
            return
        result.append(node.val)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def postorder(self) -> list:
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result) -> None:
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.val)

    def level_order(self) -> list:
        result = []
        if self.is_empty():
            return result

        queue = Queue()
        queue.enqueue(self.root)
        while not queue.is_empty():
            node = queue.dequeue()
            result.append(node.val)
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)
        return result

    def size(self) -> int:
        return self._size(self.root)

    def _size(self, node) -> int:
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def height(self) -> int:
        return self._height(self.root)

    def _height(self, node) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def __len__(self) -> int:
        return self.size()


class BinarySearchTree(BinaryTree):

    def find(self, x) -> TreeNode | None:  # O(h)
        node = self.root
        while node is not None:
            if x == node.val:
                return node
            if x > node.val:
                node = node.right
            else:
                node = node.left
        return None

    def contains(self, x) -> bool:  # O(h)
        return self.find(x) is not None

    def insert(self, x) -> None:  # O(h)
        self.root = self._insert(self.root, x)

    def _insert(self, node, x) -> TreeNode:
        if node is None:
            return TreeNode(x)
        if x < node.val:
            node.left = self._insert(node.left, x)
        elif x > node.val:
            node.right = self._insert(node.right, x)
        return node  # x already in the tree - no duplicates

    def minimum(self):  # O(h) - go left as far as possible
        if self.is_empty():
            raise ValueError("minimum of an empty tree")
        return self._min_node(self.root).val

    def maximum(self):  # O(h) - go right as far as possible
        if self.is_empty():
            raise ValueError("maximum of an empty tree")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.val

    @staticmethod
    def _min_node(node: TreeNode) -> TreeNode:
        while node.left is not None:
            node = node.left
        return node

    def delete(self, x) -> None:  # O(h)
        self.root = self._delete(self.root, x)

    def _delete(self, node, x) -> TreeNode | None:
        if node is None:  # x is not in the tree
            return None

        if x < node.val:
            node.left = self._delete(node.left, x)
        elif x > node.val:
            node.right = self._delete(node.right, x)
        else:
            # Case 1 + 2: zero or one child - replace the node with its child.
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children - copy the successor (min of the right subtree)
            # into this node, then delete the successor from the right subtree.
            successor = self._min_node(node.right)
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)
        return node
