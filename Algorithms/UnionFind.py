class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def groups(self):
        out = {}
        for x in range(len(self.parent)):
            out.setdefault(self.find(x), []).append(x)
        return list(out.values())

def kruskal(n, edges):
    uf = UnionFind(n)
    tree, total = [], 0
    for w, a, b in sorted(edges):
        if uf.union(a, b):
            tree.append((a, b, w))
            total += w
    return tree, total

edges = [(4, 0, 1), (8, 0, 2), (1, 1, 2), (2, 2, 3), (7, 3, 4), (3, 2, 4), (9, 4, 5), (5, 3, 5)]

uf = UnionFind(6)
for _, a, b in edges[:3]:
    uf.union(a, b)
print("Components:", uf.groups())
print("0 and 2 connected:", uf.connected(0, 2))
print("0 and 5 connected:", uf.connected(0, 5))

tree, total = kruskal(6, edges)
print("\nMinimum spanning tree:")
for a, b, w in tree:
    print(f"  {a} -- {b}  (weight {w})")
print("Total weight:", total)
