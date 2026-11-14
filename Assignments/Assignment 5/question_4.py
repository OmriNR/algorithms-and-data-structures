from DataStructures.graph import AdjacencyListGraph
INF = float("inf")

def find_even_minimal_ways(graph: AdjacencyListGraph, s):
    biparitite_graph = build_bipartite_graph(graph)

    orig_n = len(graph)
    bipartite_n = len(biparitite_graph)

    dist = [INF] * bipartite_n
    dist[2 * s] = 0

    for _ in range(bipartite_n - 1):
        changed = False
        for u, v, w in bipartite_graph.edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

    event_distances = [dist[2 * v] for v in range(orig_n)]
    return event_distances

def build_bipartite_graph(original_graph: AdjacencyListGraph) -> AdjacencyListGraph:
    n = len(original_graph)

    bipartite_graph = AdjacencyListGraph(2 * n)

    for u in range(n):
        for v,w in original_graph.neighbors(u):
            bipartite_graph.add_edge(2 * u, 2 * v + 1, w)
            bipartite_graph.add_edge(2 * u + 1, 2 * v, w)
    return bipartite_graph