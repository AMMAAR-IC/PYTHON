import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# Load Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Step 1: Standardize the Data
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

# Step 2: Compute Covariance Matrix
cov_matrix = np.cov(X_std.T)

# Step 3: Compute Eigenvalues and Eigenvectors
eig_vals, eig_vecs = np.linalg.eig(cov_matrix)

# Step 4: Sort Eigenvectors by Eigenvalues
sorted_indices = np.argsort(eig_vals)[::-1]
eig_vals_sorted = eig_vals[sorted_indices]
eig_vecs_sorted = eig_vecs[:, sorted_indices]

# Step 5: Select top k eigenvectors (k=2)
k = 2
W = eig_vecs_sorted[:, :k]

# Step 6: Project the data
X_pca = X_std @ W

# Step 7: Plotting
plt.figure(figsize=(8,6))
for target in np.unique(y):
    plt.scatter(X_pca[y == target, 0], X_pca[y == target, 1], label=iris.target_names[target])
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Projection (from scratch)")
plt.legend()
plt.grid(True)
plt.show()
