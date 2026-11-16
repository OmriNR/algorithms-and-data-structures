class FibonacciNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value      
        self.degree = 0         
        self.marked = False     
        self.parent = None      
        self.child = None       
        self.left = self        
        self.right = self       


class FibonacciHeap:
    def __init__(self):
        self.min_node = None 
        self.total_nodes = 0    

    def is_empty(self) -> bool:
        return self.min_node is None

    def insert(self, key, value=None) -> FibonacciNode:
        node = FibonacciNode(key, value)
        if self.min_node is None:
            self.min_node = node
        else:
            self._add_to_root_list(node)
            if key < self.min_node.key:
                self.min_node = node
        
        self.total_nodes += 1
        return node

    def get_min(self):
        if self.min_node is None:
            return None
        return (self.min_node.key, self.min_node.value)

    def union(self, other_heap):
        if other_heap.min_node is None:
            return
        if self.min_node is None:
            self.min_node = other_heap.min_node
            self.total_nodes = other_heap.total_nodes
            return

        min1 = self.min_node
        min2 = other_heap.min_node
        
        right1 = min1.right
        left2 = min2.left
        
        min1.right = min2
        min2.left = min1
        right1.left = left2
        left2.right = right1

        if other_heap.min_node.key < self.min_node.key:
            self.min_node = other_heap.min_node
            
        self.total_nodes += other_heap.total_nodes

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = [z.child]
                curr = z.child.right
                while curr != z.child:
                    children.append(curr)
                    curr = curr.right
                
                for child in children:
                    self._remove_from_child_list(child)
                    self._add_to_root_list(child)
                    child.parent = None

            self._remove_from_root_list(z)
            
            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()
                
            self.total_nodes -= 1
            return (z.key, z.value)
        return None


    def _add_to_root_list(self, node):
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node

    def _remove_from_root_list(self, node):
        if node == node.right:
            return
        node.left.right = node.right
        node.right.left = node.left

    def _add_child(self, parent, child):
        child.parent = parent
        parent.degree += 1
        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child

    def _remove_from_child_list(self, node):
        parent = node.parent
        parent.degree -= 1
        if parent.child == node:
            if node.right == node:
                parent.child = None
            else:
                parent.child = node.right
        node.left.right = node.right
        node.right.left = node.left

    def _consolidate(self):
        max_degree = int(self.total_nodes.bit_length() * 2) + 1
        table = [None] * max_degree

        # איסוף כל השורשים הנוכחיים
        root_list = [self.min_node]
        curr = self.min_node.right
        while curr != self.min_node:
            root_list.append(curr)
            curr = curr.right

        for w in root_list:
            d = w.degree
            while table[d] is not None:
                other = table[d]
                if w.key > other.key:
                    w, other = other, w
                self._link(other, w)
                table[d] = None
                d += 1
            table[d] = w

        self.min_node = None
        for w in table:
            if w is not None:
                if self.min_node is None:
                    self.min_node = w
                    w.left = w
                    w.right = w
                else:
                    self._add_to_root_list(w)
                    if w.key < self.min_node.key:
                        self.min_node = w

    def _link(self, ptr2, ptr1):
        self._remove_from_root_list(ptr2)
        self._add_child(ptr1, ptr2)
        ptr2.marked = False