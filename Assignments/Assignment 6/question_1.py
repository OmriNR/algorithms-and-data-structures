from DataStructures.graph import Graph

def find_graph_center(graph: Graph):
    dist_matrix = floyd_warshall(graph)

    n = len(dist_matrix)
    best_vertex = -1
    min_eccentricity = float('inf')

    for u in range(n):
        eccentricity = max(dist[u])

        if eccentricity < min_eccentricity:
            min_eccentricity = eccentricity
            best_vertex = u

    return best_vertex, min_eccentricity
 
def floyd_warshall(graph: Graph):  # O(V^3)
    n = len(graph)
    INF = float('inf')

    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0

    nxt = [[None] * n for _ in range(n)]

    edges = list(graph.edges)
    if not graph.directed:
        edges += [(v, u, w) for u, v, w in graph.edges]

    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v] = v

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]

    return dist, nxt

def add_edge(dist, u, v, w):
    if w >= dist[u][v]:
        return

    n = len(dist)
    for i in range(n):
        for j in range(n):
            new_dist = dist[i][u] + w + dist[v][j]
            if new_dist < dist[i][j]:
                dist[i][j] = new_dist