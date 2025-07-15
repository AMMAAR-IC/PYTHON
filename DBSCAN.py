import numpy as np
from collections import deque

class DBSCAN:
    """
    Density‑based clustering.
      • eps:   neighborhood radius
      • min_pts: minimum points to form a dense region (core)

    Labels:
      0 … k‑1  → cluster IDs
      -1       → noise
    """

    def __init__(self, eps=0.5, min_pts=5):
        self.eps = eps
        self.min_pts = min_pts
        self.labels_ = None

    def _region_query(self, dists, idx):
        """Indices of points within eps of point idx."""
        return np.where(dists[idx] <= self.eps)[0]

    def fit(self, X):
        n = X.shape[0]
        self.labels_ = np.full(n, -1, dtype=int)     # start as noise
        visited = np.zeros(n, dtype=bool)

        # Pre‑compute full distance matrix (O(n²) memory; fine for small/med sets)
        dists = np.linalg.norm(X[:, None] - X[None, :], axis=2)

        cluster_id = 0
        for i in range(n):
            if visited[i]:
                continue
            visited[i] = True
            neighbors = self._region_query(dists, i)

            if neighbors.size < self.min_pts:        # not a core point
                continue

            # Start new cluster
            self.labels_[i] = cluster_id
            queue = deque(neighbors)

            while queue:
                j = queue.popleft()

                if not visited[j]:
                    visited[j] = True
                    j_neighbors = self._region_query(dists, j)
                    if j_neighbors.size >= self.min_pts:
                        queue.extend(j_neighbors)

                if self.labels_[j] == -1:            # unassigned → add to cluster
                    self.labels_[j] = cluster_id

            cluster_id += 1
        return self

    def predict(self, X_new):
        raise NotImplementedError("DBSCAN is unsupervised; call fit() and use labels_.")
        import numpy as np
from collections import deque


class DBSCAN:
    """
    Density‑based clustering.
      • eps:   neighborhood radius
      • min_pts: minimum points to form a dense region (core)

    Labels:
      0 … k‑1  → cluster IDs
      -1       → noise
    """

    def __init__(self, eps=0.5, min_pts=5):
        self.eps = eps
        self.min_pts = min_pts
        self.labels_ = None

    def _region_query(self, dists, idx):
        """Indices of points within eps of point idx."""
        return np.where(dists[idx] <= self.eps)[0]

    def fit(self, X):
        n = X.shape[0]
        self.labels_ = np.full(n, -1, dtype=int)     # start as noise
        visited = np.zeros(n, dtype=bool)

        # Pre‑compute full distance matrix (O(n²) memory; fine for small/med sets)
        dists = np.linalg.norm(X[:, None] - X[None, :], axis=2)

        cluster_id = 0
        for i in range(n):
            if visited[i]:
                continue
            visited[i] = True
            neighbors = self._region_query(dists, i)

            if neighbors.size < self.min_pts:        # not a core point
                continue

            # Start new cluster
            self.labels_[i] = cluster_id
            queue = deque(neighbors)

            while queue:
                j = queue.popleft()

                if not visited[j]:
                    visited[j] = True
                    j_neighbors = self._region_query(dists, j)
                    if j_neighbors.size >= self.min_pts:
                        queue.extend(j_neighbors)

                if self.labels_[j] == -1:            # unassigned → add to cluster
                    self.labels_[j] = cluster_id

            cluster_id += 1
        return self

    def predict(self, X_new):
        raise NotImplementedError("DBSCAN is unsupervised; call fit() and use labels_.")
        

# ───────────────────────────── quick demo ─────────────────────────────
if __name__ == "__main__":
    # Two noisy concentric circles (classic DBSCAN example)
    from sklearn.datasets import make_circles
    X, _ = make_circles(n_samples=600, factor=.5, noise=.05, random_state=0)

    model = DBSCAN(eps=0.15, min_pts=4)
    model.fit(X)
    print("Cluster labels (-1 = noise):")
    print(model.labels_)

if __name__ == "__main__":
    # Two noisy concentric circles (classic DBSCAN example)
    from sklearn.datasets import make_circles
    X, _ = make_circles(n_samples=600, factor=.5, noise=.05, random_state=0)

    model = DBSCAN(eps=0.15, min_pts=4)
    model.fit(X)
    print("Cluster labels (-1 = noise):")
    print(model.labels_)
