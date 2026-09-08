from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
X, y = X[y != 2], y[y != 2]  # Keep only 2 classes: 0 and 1

model = LogisticRegression()
model.fit(X, y)

print("Prediction:", model.predict([X[0]]))
print("Probability:", model.predict_proba([X[0]]))
