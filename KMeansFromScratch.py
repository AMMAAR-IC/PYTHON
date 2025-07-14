import random
import numpy as np

def k_means(X, k, max_iter=100):
    centroids = X[random.sample(range(len(X)), k)]
    for _ in range(max_iter):
        clusters = [[] for _ in range(k)]
        for x in X:
            idx = np.argmin([np.linalg.norm(x - c) for c in centroids])
            clusters[idx].append(x)
        new_centroids = [np.mean(cluster, axis=0) if cluster else centroids[i]
                         for i, cluster in enumerate(clusters)]
        if np.allclose(centroids, new_centroids): break
        centroids = new_centroids
    return centroids, clusters
