import numpy as np

class DecisionStump:
    """
    One‑dimensional, inequality‑based weak learner.

    Learns:  sign( (x[:, feature] ? thresh) ^ polarity )
    where polarity ∈ {+1, ‑1} chooses < or >, whichever minimizes error.
    """

    def __init__(self):
        self.feature = None
        self.threshold = None
        self.polarity = 1

    def fit(self, X, y, sample_weight):
        m, n = X.shape
        best_err = np.inf

        # Iterate over every feature and unique threshold.
        for j in range(n):
            thresholds = np.unique(X[:, j])
            for thresh in thresholds:
                for polarity in (+1, -1):
                    pred = np.ones(m)
                    if polarity == 1:
                        pred[X[:, j] < thresh] = -1
                    else:
                        pred[X[:, j] > thresh] = -1

                    err = np.sum(sample_weight[pred != y])
                    if err < best_err:
                        best_err = err
                        self.feature = j
                        self.threshold = thresh
                        self.polarity = polarity

    def predict(self, X):
        m = X.shape[0]
        pred = np.ones(m)
        if self.polarity == 1:
            pred[X[:, self.feature] < self.threshold] = -1
        else:
            pred[X[:, self.feature] > self.threshold] = -1
        return pred


class AdaBoost:
    """
    AdaBoost ensemble with decision stumps.
    """

    def __init__(self, n_estimators=50):
        self.n_estimators = n_estimators
        self.stumps = []
        self.alphas = []

    def fit(self, X, y):
        y = y.astype(float)
        y[y == 0] = -1            # ensure labels are ±1
        m = X.shape[0]
        w = np.full(m, 1 / m)     # initial uniform weights

        for _ in range(self.n_estimators):
            stump = DecisionStump()
            stump.fit(X, y, w)
            pred = stump.predict(X)

            # Weighted error & model weight
            err = np.sum(w[pred != y])
            err = np.clip(err, 1e-10, 1 - 1e-10)  # avoid div/0
            alpha = 0.5 * np.log((1 - err) / err)

            # Weight update
            w *= np.exp(-alpha * y * pred)
            w /= np.sum(w)

            # Store
            self.stumps.append(stump)
            self.alphas.append(alpha)

    def predict(self, X):
        final = sum(alpha * stump.predict(X)
                    for stump, alpha in zip(self.stumps, self.alphas))
        return (np.sign(final) + 1) // 2  # back to {0,1}
