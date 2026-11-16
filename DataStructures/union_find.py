class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int):
        if self.parent[i] == i:
            return i

        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i : int, j: int):

        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

    def connected(self, i: int, j: int):
        return self.find(i) == self.find(j)