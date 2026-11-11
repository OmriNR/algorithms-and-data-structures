from DataSturctures.graph import Graph
from DataSturctures.heap import MinHeap

INF = float("inf")

def dijkesrta(graph: Graph, s: int = 0):
    n = len(graph)
    dist = [INF] * n
    parent = [None] * n
    done = [False] * n

    dist[s] = 0
    heap = MinHeap()
    heap.insert((0,s))

    while not heap.is_empty():
        d, u = heap.extract_min()
        if done[u]:
            continue
        done[u] = True

        for v in graph.neighbors(u):
            w = graph.weight(u, v)
            if w < 0:
                raise ValueError("DIjkstera does not work with negative weights")

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heap.insert((dist[v], v))

    return dist, parent

def beam_search(graph: Graph, s: int, goal: int, h, beam_width: int = 2):
    n = len(graph)
    visited = [False] * n
    parent = [None] * n

    visited[s] = True
    beam = [s]

    while beam:
        candidates = MinHeap()

        for u in beam:
            if u == goal:
                return get_path(parent, s, goal)
            for v in graph.neighbors(u):
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    candidates.insert((h(v), v))
        beam = []
        while not candidates.is_empty() and len(beam) < beam_width:
            _, v = candidates.extract_min()
            beam.append(v)

def a_star(graph: Graph, s: int, goal: int, h):
    n = len(graph)
    g_cost = [INF] * n  # g(v) = best known distance s -> v
    parent = [None] * n
    closed = [False] * n

    g_cost[s] = 0
    heap = MinHeap()
    heap.insert((h(s), s))  # (f = g + h, vertex)

    while not heap.is_empty():
        f, u = heap.extract_min()
        if closed[u]:  # old entry
            continue
        if u == goal:
            return get_path(parent, s, goal), g_cost[goal]
        closed[u] = True

        for v in graph.neighbors(u):
            new_g = g_cost[u] + graph.weight(u, v)
            if new_g < g_cost[v]:
                g_cost[v] = new_g
                parent[v] = u
                closed[v] = False  # reopen v if a shorter path to it was found
                heap.insert((new_g + h(v), v))

    return [], INF

def bellman_ford(graph: Graph, s: int = 0):  # O(|V| * |E|)
    n = len(graph)

    # every edge in its direction (an undirected edge appears in both directions)
    edges = []
    for u in range(n):
        for v in graph.neighbors(u):
            edges.append((u, v, graph.weight(u, v)))

    dist = [INF] * n
    parent = [None] * n
    dist[s] = 0

    # relax all edges n - 1 times
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:  # nothing changed, so we're already done
            break

    # one more pass: if anything can still get shorter, there is a negative cycle
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise ValueError("graph contains a negative cycle")

    return dist, parent

def get_path(parent, s: int, t: int):
    path = []
    curr = t
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path if path[0] == s else []