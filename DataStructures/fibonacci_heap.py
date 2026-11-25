class FibNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.children = []
        self.marked = False  # "שחור": איבד ילד מאז שהפך לילד של מישהו


class FibonacciHeap:
    def __init__(self):
        self.roots = []       # השכבה העליונה (כל העצים)
        self.min_node = None  # מצביע למינימום

    def is_empty(self):
        return self.min_node is None

    def get_min(self):
        return self.min_node

    def insert(self, key, value=None):
        node = FibNode(key, value)
        self.roots.append(node)
        if self.min_node is None or key < self.min_node.key:
            self.min_node = node
        return node

    def union(self, other):
        self.roots.extend(other.roots)
        if other.min_node is not None and (self.min_node is None or other.min_node.key < self.min_node.key):
            self.min_node = other.min_node
        other.roots, other.min_node = [], None

    def extract_min(self):
        z = self.min_node
        if z is None:
            return None
        self.roots.remove(z)
        for child in z.children:  # הילדים עולים לשכבה העליונה
            child.parent = None
            child.marked = False
        self.roots.extend(z.children)
        z.children = []
        self._consolidate()
        return z

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("המפתח החדש חייב להיות קטן או שווה לישן")
        node.key = new_key
        parent = node.parent
        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        if node.key < self.min_node.key:
            self.min_node = node

    def delete(self, node):
        parent = node.parent
        if parent is not None:
            self._cut(node, parent)
            self._cascading_cut(parent)
        self.min_node = node  # מעבירים אותו למינימום ומוציאים
        self.extract_min()

    def _consolidate(self):
        # מחברים שורשים עם אותה דרגה, עד שכל דרגה מופיעה לכל היותר פעם אחת
        by_degree = {}
        for w in self.roots:
            while len(w.children) in by_degree:
                other = by_degree.pop(len(w.children))
                if other.key < w.key:
                    w, other = other, w
                self._link(other, w)
            by_degree[len(w.children)] = w
        self.roots = list(by_degree.values())
        self.min_node = min(self.roots, key=lambda n: n.key, default=None)

    def _link(self, child, parent):
        child.parent = parent
        parent.children.append(child)

    def _cut(self, node, parent):
        parent.children.remove(node)
        node.parent = None
        node.marked = False
        self.roots.append(node)

    def _cascading_cut(self, node):
        parent = node.parent
        if parent is None:
            return
        if not node.marked:
            node.marked = True
        else:
            self._cut(node, parent)
            self._cascading_cut(parent)