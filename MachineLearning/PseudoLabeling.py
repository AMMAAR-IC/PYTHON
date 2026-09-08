from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Create synthetic data
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_unlabeled, y_train, _ = train_test_split(X, y, train_size=0.1, random_state=42)

# Train on small labeled set
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict unlabeled
pseudo_probs = model.predict_proba(X_unlabeled)
pseudo_labels = model.predict(X_unlabeled)
confident = np.max(pseudo_probs, axis=1) > 0.9

# Add confident pseudo-labels to training set
X_combined = np.vstack([X_train, X_unlabeled[confident]])
y_combined = np.concatenate([y_train, pseudo_labels[confident]])

# Retrain
model.fit(X_combined, y_combined)
y_pred = model.predict(X)
print("Pseudo-Labeling Accuracy:", accuracy_score(y, y_pred))
