from sklearn.datasets import load_iris
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)

# Hide labels
rng = np.random.RandomState(0)
y_semi = np.copy(y)
mask = rng.rand(len(y)) < 0.7
y_semi[mask] = -1  # unlabeled

# Self-training with Decision Tree as base
base_clf = DecisionTreeClassifier()
self_training_model = SelfTrainingClassifier(base_clf)
self_training_model.fit(X, y_semi)

print("Self-Training Accuracy:", accuracy_score(y, self_training_model.predict(X)))
