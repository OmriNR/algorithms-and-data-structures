from DataSturctures.graph import Graph
from DataSturctures.queue import Queue
from DataSturctures.stack import Stack

WHITE, GRAY, BLACK = 0, 1, 2   # not discovered / discovered / finished

def bfs_graph_search(graph: Graph, s: int):
	n = len(graph)
	visited = [False] * n
	order = []
	
	queue = Queue()
	queue.enqueue(s)
	
	while not queue.is_empty():
		u = queue.dequeue()
		order.append(u)
		for v in graph.neighbors(u):
			if not visited[v]:
				visited[v] = True
				queue.enqueue(v)
	return order
	
def dfs_graph_search(g : Graph, s: int):
	n = len(g)
	visited = [False] * n
	order = []
	
	st = Stack()
	st.push(s)
	while not st.is_empty():
		u = st.pop()
		visited[u] = True
		order.append(u)
		for v in g.neighbors(u):
			if not visited[v]:
				st.push(v)
	return order