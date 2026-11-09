from DataSturctures.graph import Graph

def has_cycle_undirected(graph : Graph, V : int):
    visited = [False] * V

    def dfs(u, parent):
        visited[u] = True

        for v in graph[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
                elif v != parent:
                    return True
        return False

    for i in range(V):
        if not visited[i]:
            if dfs(i, -1):
                return True

    return False