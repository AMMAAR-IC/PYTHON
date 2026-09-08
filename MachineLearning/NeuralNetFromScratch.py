import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

def softmax(z):
    # Subtract the row max first so exp() never overflows
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)

class NeuralNetwork:
    def __init__(self, layers, lr=0.3, seed=42):
        self.layers = layers
        self.lr = lr
        rng = np.random.default_rng(seed)
        # He initialisation - keeps the activation variance stable through ReLU layers
        self.weights = [rng.normal(0, np.sqrt(2 / layers[i]), (layers[i], layers[i + 1]))
                        for i in range(len(layers) - 1)]
        self.biases = [np.zeros(n) for n in layers[1:]]

    def forward(self, X):
        # Every activation is kept, backward() needs them for the chain rule
        activations = [X]
        a = X
        last = len(self.weights) - 1
        for i, (W, b) in enumerate(zip(self.weights, self.biases)):
            z = a @ W + b
            a = softmax(z) if i == last else np.maximum(0, z)
            activations.append(a)
        return activations

    def backward(self, activations, y_onehot):
        # Softmax + cross-entropy collapse into this one clean output delta
        delta = (activations[-1] - y_onehot) / len(y_onehot)
        for i in reversed(range(len(self.weights))):
            grad_w = activations[i].T @ delta
            grad_b = delta.sum(axis=0)
            if i > 0:
                # Propagate through the old weights before overwriting them,
                # then mask where the ReLU was inactive
                delta = (delta @ self.weights[i].T) * (activations[i] > 0)
            self.weights[i] -= self.lr * grad_w
            self.biases[i] -= self.lr * grad_b

    def fit(self, X, y, epochs=100, batch_size=32, verbose=10):
        y_onehot = np.eye(self.layers[-1])[y]
        rng = np.random.default_rng(0)
        for epoch in range(1, epochs + 1):
            order = rng.permutation(len(X))
            for start in range(0, len(X), batch_size):
                batch = order[start:start + batch_size]
                self.backward(self.forward(X[batch]), y_onehot[batch])
            if verbose and epoch % verbose == 0:
                probs = self.forward(X)[-1]
                loss = -np.mean(np.log(probs[np.arange(len(y)), y] + 1e-9))
                acc = np.mean(probs.argmax(axis=1) == y)
                print(f"Epoch {epoch:4d} | loss {loss:.4f} | acc {acc:.4f}")

    def predict(self, X):
        return self.forward(X)[-1].argmax(axis=1)

# Load dataset - 8x8 handwritten digits, pixels are 0-16 so scale them to 0-1
digits = load_digits()
X = digits.data / 16.0
y = digits.target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train and predict
net = NeuralNetwork([64, 32, 10])
net.fit(X_train, y_train)
y_pred = net.predict(X_test)

# Accuracy
accuracy = np.mean(y_pred == y_test)
print("Test accuracy:", accuracy)
