from DataSturctures.graph import Graph
from DataSturctures.queue import Queue

def yellowest_mst(graph: Graph):
    n = len(graph)
    sorted_edges = bucket_sort_edges_two_buckets(graph.edges)

    parent = list(range(n))
    rank [0] * n

    mst = []
    total = 0
    for w, u, v in sorted_edges:
        if union(parent, rank, u, v):
            mst.append((u,v,w))
            total += w
            if (len(mst) == n -1):
                break
            
    return mst, total

def bucket_sort_edges_two_buckets(edges):
    if not edges:
        return []
    
    max_weight = max(edge[2] for edge in edges)

    yellow_buckets = [Queue for _ in range(max_weight + 1)]
    black_buckets = [Queue for _ in range(max_weight + 1)]

    for edge in edges:
        u, v, weight, color = edge
        if color == "yellow":
            yellow_buckets[weight].enqueue(edge)
        else:
            black_buckets[weight].enqueue(edge)

    sorted_edges = []
    for w in range(max_weight + 1):
        sorted_edges.extend(yellow_buckets[w])
        sorted_edges.extend(black_buckets[w])

    return sorted_edges

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