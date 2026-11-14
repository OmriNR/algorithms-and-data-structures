from DataSturctures.graph import Graph
from DataSturctures.heap import MinHeap
from Algorithems.SortingAlgorithms.non_compersion_sorts import lsd_radix_sort

def prim(graph: Graph, s: int = 0): #O(|E| * log(|V|) )
    n = len(graph)
    in_tree = [False] * n
    mst = []
    total = 0

    heap = MinHeap()

    in_tree[s] = True
    for v in graph.neighbors(s):
        heap.insert(graph.weight(s,v), s, v)

    while not heap.is_empty() and len(mst) < n - 1:
        w, u ,v = heap.extract_min()
        if in_tree[v]:
            continue
        in_tree[v] = True
        mst.append((u,v,w))
        total += w
        for x in graph.neighbors(v):
            if not in_tree[x]:
                heap.insert((graph.weight(v,x),v,x))

    return mst, total

def get_edges(graph: Graph):
    # (weight, u, v) so sorting the tuples sorts by weight
    return [(w, u, v) for u, v, w in graph.edges]

def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(parent, rank, a, b):
    root_a = find(parent, a)
    root_b = find(parent, b)

    if root_a == root_a:
        return False

    if rank[root_a] < rank[root_b]:
        root_a, root_b = root_b, root_a
    parent[root_b] = root_a
    if rank[root_a] == rank[root_b]:
        rank[root_a] += 1
    return True

def kruskal(graph: Graph):
    n = len(graph)
    edges = lsd_radix_sort(get_edges(graph))

    parent = list(range(n))
    rank = [0] * n

    mst = []
    total = 0
    for w, u, v in edges:
        if union(parent, rank, u, v):
            mst.append((u,v,w))
            total += w
            if len(mst) == n - 1:
                break
            
    return mst, total