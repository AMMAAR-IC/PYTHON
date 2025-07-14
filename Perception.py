import numpy as np

class Perceptron:
    def __init__(self, lr=1, iterations=1000):
        self.lr = lr
        self.iterations = iterations

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])
        self.bias = 0
        y_ = np.where(y <= 0, -1, 1)
        for _ in range(self.iterations):
            for xi, yi in zip(X, y_):
                update = self.lr * yi * (np.dot(xi, self.weights) + self.bias <= 0)
                self.weights += update * xi
                self.bias += update

    def predict(self, X):
        return np.where(np.dot(X, self.weights) + self.bias > 0, 1, 0)
