
def _find_edge_index(edges: list, u: int, v: int, directed: bool) -> int:  # O(m)
    """Position of the edge (u, v) in an edge list, or -1 if it isn't there.
    In an undirected graph (u, v) and (v, u) are the same edge."""
    for i, (a, b, _) in enumerate(edges):
        if (a == u and b == v) or (not directed and a == v and b == u):
            return i
    return -1


# ======================================================================
# 1. Adjacency matrix
# ======================================================================

class AdjacencyMatrixGraph:
    def __init__(self, n: int, directed: bool = False):  # O(n^2)
        self.n = n
        self.directed = directed
        self.matrix = [[None] * n for _ in range(n)]
        self.edges = []  # E: every edge once, as (u, v, weight)

    def _check_vertex(self, v: int) -> None:
        if v < 0 or v >= self.n:
            raise IndexError(f"vertex {v} is not in the graph (0..{self.n - 1})")

    def _record_edge(self, u: int, v: int, weight, existed: bool) -> None:
        """Keep self.edges in sync: append a new edge (O(1)) or update an existing one's weight (O(m))."""
        if existed:
            i = _find_edge_index(self.edges, u, v, self.directed)
            a, b, _ = self.edges[i]
            self.edges[i] = (a, b, weight)
        else:
            self.edges.append((u, v, weight))

    def has_edge(self, u: int, v: int) -> bool:  # O(1)
        """Is there an edge from u to v? (In an undirected graph the direction doesn't matter.)"""
        self._check_vertex(u)
        self._check_vertex(v)
        return self.matrix[u][v] is not None

    def are_neighbors(self, u: int, v: int) -> bool:  # O(1)
        """Are u and v connected by an edge in any direction?"""
        return self.has_edge(u, v) or self.has_edge(v, u)

    def add_edge(self, u: int, v: int, weight=1) -> None:  # O(1) new edge, O(m) weight update
        """Add the edge (u, v). If it already exists, its weight is updated."""
        self._check_vertex(u)
        self._check_vertex(v)
        if u == v:
            raise ValueError("loops are not allowed in a simple graph")

        self._record_edge(u, v, weight, existed=self.matrix[u][v] is not None)
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight  # keep A = A^T

    def delete_edge(self, u: int, v: int) -> None:  # O(m) - removing from the edge list
        if not self.has_edge(u, v):
            raise ValueError(f"edge ({u}, {v}) is not in the graph")

        self.matrix[u][v] = None
        if not self.directed:
            self.matrix[v][u] = None
        self.edges.pop(_find_edge_index(self.edges, u, v, self.directed))

    def weight(self, u: int, v: int):  # O(1)
        if not self.has_edge(u, v):
            raise ValueError(f"edge ({u}, {v}) is not in the graph")
        return self.matrix[u][v]

    def out_degree(self, v: int) -> int:  # O(n) - count the cells in row v
        self._check_vertex(v)
        count = 0
        for j in range(self.n):
            if self.matrix[v][j] is not None:
                count += 1
        return count

    def in_degree(self, v: int) -> int:  # O(n) - count the cells in column v
        self._check_vertex(v)
        count = 0
        for i in range(self.n):
            if self.matrix[i][v] is not None:
                count += 1
        return count

    def degree(self, v: int) -> int:  # O(n)
        if self.directed:
            return self.in_degree(v) + self.out_degree(v)
        return self.out_degree(v)  # row = column, so counting the row is enough

    def neighbors(self, v: int) -> list[int]:  # O(n)
        """The vertices v has an edge to (out-neighbours in a directed graph)."""
        self._check_vertex(v)
        result = []
        for j in range(self.n):
            if self.matrix[v][j] is not None:
                result.append(j)
        return result

    def __len__(self) -> int:
        return self.n

    def __repr__(self) -> str:
        rows = []
        for i in range(self.n):
            cells = []
            for j in range(self.n):
                cells.append("." if self.matrix[i][j] is None else str(self.matrix[i][j]))
            rows.append(f"{i}: " + " ".join(cells))
        kind = "directed" if self.directed else "undirected"
        return f"AdjacencyMatrixGraph({kind}, n={self.n})\n" + "\n".join(rows)


# ======================================================================
# 2. Adjacency list (array of linked lists)
# ======================================================================

class _EdgeNode:
    """A node in a vertex's neighbour list: the neighbour, the edge weight and the next node."""

    def __init__(self, vertex: int, weight, next_node=None):
        self.vertex = vertex
        self.weight = weight
        self.next = next_node


class AdjacencyListGraph:
    def __init__(self, n: int, directed: bool = False):  # O(n)
        self.n = n
        self.directed = directed
        self.heads = [None] * n  # heads[u] = first node of u's neighbour list
        self.edges = []  # E: every edge once, as (u, v, weight)

    def _check_vertex(self, v: int) -> None:
        if v < 0 or v >= self.n:
            raise IndexError(f"vertex {v} is not in the graph (0..{self.n - 1})")

    def _find(self, u: int, v: int) -> _EdgeNode | None:  # O(deg(u)) - scan u's list for v
        node = self.heads[u]
        while node is not None:
            if node.vertex == v:
                return node
            node = node.next
        return None

    def _insert(self, u: int, v: int, weight) -> None:  # O(deg(u))
        existing = self._find(u, v)
        if existing is not None:  # no double edges - just update the weight
            existing.weight = weight
        else:
            self.heads[u] = _EdgeNode(v, weight, self.heads[u])  # insert at the head, O(1)

    def _remove(self, u: int, v: int) -> bool:  # O(deg(u))
        prev = None
        node = self.heads[u]
        while node is not None:
            if node.vertex == v:
                if prev is None:
                    self.heads[u] = node.next
                else:
                    prev.next = node.next
                return True
            prev = node
            node = node.next
        return False

    def _record_edge(self, u: int, v: int, weight, existed: bool) -> None:
        """Keep self.edges in sync: append a new edge (O(1)) or update an existing one's weight (O(m))."""
        if existed:
            i = _find_edge_index(self.edges, u, v, self.directed)
            a, b, _ = self.edges[i]
            self.edges[i] = (a, b, weight)
        else:
            self.edges.append((u, v, weight))

    def has_edge(self, u: int, v: int) -> bool:  # O(deg(u))
        """Is there an edge from u to v? (In an undirected graph the direction doesn't matter.)"""
        self._check_vertex(u)
        self._check_vertex(v)
        return self._find(u, v) is not None

    def are_neighbors(self, u: int, v: int) -> bool:  # O(deg(u) + deg(v))
        """Are u and v connected by an edge in any direction?"""
        return self.has_edge(u, v) or self.has_edge(v, u)

    def add_edge(self, u: int, v: int, weight=1) -> None:  # O(deg(u) + deg(v)), O(m) for a weight update
        """Add the edge (u, v). If it already exists, its weight is updated."""
        self._check_vertex(u)
        self._check_vertex(v)
        if u == v:
            raise ValueError("loops are not allowed in a simple graph")

        self._record_edge(u, v, weight, existed=self._find(u, v) is not None)
        self._insert(u, v, weight)
        if not self.directed:
            self._insert(v, u, weight)  # undirected: stored in both lists

    def delete_edge(self, u: int, v: int) -> None:  # O(m) - removing from the edge list
        self._check_vertex(u)
        self._check_vertex(v)
        if not self._remove(u, v):
            raise ValueError(f"edge ({u}, {v}) is not in the graph")
        if not self.directed:
            self._remove(v, u)
        self.edges.pop(_find_edge_index(self.edges, u, v, self.directed))

    def weight(self, u: int, v: int):  # O(deg(u))
        self._check_vertex(u)
        self._check_vertex(v)
        node = self._find(u, v)
        if node is None:
            raise ValueError(f"edge ({u}, {v}) is not in the graph")
        return node.weight

    def out_degree(self, v: int) -> int:  # O(deg(v)) - length of v's list
        self._check_vertex(v)
        count = 0
        node = self.heads[v]
        while node is not None:
            count += 1
            node = node.next
        return count

    def in_degree(self, v: int) -> int:  # O(n + m) - v can appear in any other list
        self._check_vertex(v)
        if not self.directed:
            return self.out_degree(v)
        count = 0
        for u in range(self.n):
            if self._find(u, v) is not None:
                count += 1
        return count

    def degree(self, v: int) -> int:
        if self.directed:
            return self.in_degree(v) + self.out_degree(v)  # O(n + m)
        return self.out_degree(v)  # O(deg(v))

    def neighbors(self, v: int) -> list[int]:  # O(deg(v))
        """The vertices v has an edge to (out-neighbours in a directed graph)."""
        self._check_vertex(v)
        result = []
        node = self.heads[v]
        while node is not None:
            result.append(node.vertex)
            node = node.next
        return result

    def __len__(self) -> int:
        return self.n

    def __repr__(self) -> str:
        rows = []
        for u in range(self.n):
            parts = []
            node = self.heads[u]
            while node is not None:
                parts.append(str(node.vertex) if node.weight == 1 else f"{node.vertex}(w={node.weight})")
                node = node.next
            rows.append(f"{u}: " + " -> ".join(parts))
        kind = "directed" if self.directed else "undirected"
        return f"AdjacencyListGraph({kind}, n={self.n})\n" + "\n".join(rows)


# Default graph: the adjacency list is better for sparse graphs (most graphs in practice).
Graph = AdjacencyListGraph
