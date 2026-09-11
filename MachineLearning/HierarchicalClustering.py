import numpy as np

def agglomerative(X, k, linkage='average'):
    clusters = [[i] for i in range(len(X))]
    merges = []

    while len(clusters) > k:
        best, pair = np.inf, None
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                d = cluster_distance(X, clusters[i], clusters[j], linkage)
                if d < best:
                    best, pair = d, (i, j)
        i, j = pair
        merges.append((clusters[i], clusters[j], best))
        clusters[i] = clusters[i] + clusters[j]
        clusters.pop(j)

    labels = np.empty(len(X), dtype=int)
    for label, cluster in enumerate(clusters):
        labels[cluster] = label
    return labels, merges

def cluster_distance(X, a, b, linkage):
    d = np.linalg.norm(X[a][:, None] - X[b][None, :], axis=-1)
    if linkage == 'single':
        return d.min()
    if linkage == 'complete':
        return d.max()
    return d.mean()  # average linkage

def print_dendrogram(merges):
    for a, b, d in merges:
        print(f"  {sorted(a)} + {sorted(b)}  at distance {d:.2f}")

rng = np.random.default_rng(0)
X = np.vstack([rng.normal([0, 0], 0.4, (8, 2)),
               rng.normal([4, 4], 0.4, (8, 2)),
               rng.normal([8, 0], 0.4, (8, 2))])

for linkage in ('single', 'complete', 'average'):
    labels, merges = agglomerative(X, k=3, linkage=linkage)
    sizes = np.bincount(labels)
    print(f"{linkage:>8} linkage -> cluster sizes {sizes.tolist()}")

labels, merges = agglomerative(X[:6], k=1)
print("\nMerge order for the first 6 points:")
print_dendrogram(merges)
