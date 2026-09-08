from sklearn.semi_supervised import LabelSpreading
from sklearn import datasets
from sklearn.metrics import accuracy_score
import numpy as np

digits = datasets.load_digits()
X, y = digits.data, digits.target

rng = np.random.RandomState(42)
y_spread = -np.ones_like(y)
n_labeled = int(0.1 * len(y))
labeled_indices = rng.choice(len(y), n_labeled, replace=False)
y_spread[labeled_indices] = y[labeled_indices]

model = LabelSpreading(kernel='knn', n_neighbors=7)
model.fit(X, y_spread)

accuracy = accuracy_score(y, model.transduction_)
print("Label Spreading Accuracy:", round(accuracy * 100, 2), "%")
