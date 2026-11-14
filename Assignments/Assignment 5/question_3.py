from DataStructures.graph import Graph

INF = float("inf")

def bellman_ford_max_m(graph: Graph, s, m):
    n = len(graph)

    edges = graph.edges

    dist = [INF] * n
    parent = [None] * n
    dist[s] = 0

    for _ in range(m):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break
    
    return dist, parent