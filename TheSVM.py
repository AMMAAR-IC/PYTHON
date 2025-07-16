from sklearn.svm import SVC
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = SVC(kernel='linear')  # Try also 'rbf', 'poly', etc.
model.fit(X, y)

print("Prediction:", model.predict([X[0]]))
