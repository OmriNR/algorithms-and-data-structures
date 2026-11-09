from DataSturctures.graph import Graph
from DataSturctures.queue import Queue
from DataSturctures.stack import Stack

WHITE, GRAY, BLACK = 0, 1, 2   # not discovered / discovered / finished

def bfs_graph_search(graph : Graph, s: int): 
    n = len(graph)
    color = [WHITE]
    dist = [None] * n
    parent = [None] * n
    order = []

    color[s] = GRAY

    dist[s] = 0
    q = Queue()
    q.enqueue(s)

    while not q.is_empty():
        u = q.dequeue()
        order.append(u)
        for v in graph.neighbors(u):
            if color[v] in graph.neighbors(u):
                color[v] = GRAY
                dist[v] = dist[u] + 1
                parent[v] = u
                q.enqueue(v)
        color[u] = BLACK

    return dist, parent, order

def dfs(g: Graph):
    n = len(g)
    color = [WHITE] * n
    d = [0] * n
    f = [0] * n
    parent = [None] * n
    order = []
    time = [0]                   # a 1-cell list so dfs_visit can change it

    def dfs_visit(u: int):
        time[0] += 1
        d[u] = time[0]
        color[u] = GRAY
        order.append(u)
        for v in g.neighbors(u):
            if color[v] == WHITE:
                parent[v] = u
                dfs_visit(v)
        color[u] = BLACK
        time[0] += 1
        f[u] = time[0]

    for u in range(n):
        if color[u] == WHITE:
            dfs_visit(u)

    return d, f, parent, order

def dfs_graph_search(g : Graph, s: int):
    n = len(g)
    visited = [False] * n
    order = []

    st = Stack()
    st.push(s)

    while not st.is_empty():
        u = st.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        for v in g.neighbors(u):
            if not visited[v]:
                st.push(v)

    return order