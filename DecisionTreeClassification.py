from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

X, y = load_iris(return_X_y=True)
model = DecisionTreeClassifier()
model.fit(X, y)

plt.figure(figsize=(10, 6))
plot_tree(model, filled=True, feature_names=load_iris().feature_names)
plt.show()

print("Prediction:", model.predict([X[0]]))
