from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Data
texts = ["free money now", "earn cash fast", "hello friend", "let's meet tomorrow"]
labels = [1, 1, 0, 0]  # 1 = spam, 0 = ham

# Vectorize text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Train model
model = MultinomialNB()
model.fit(X, labels)

# Predict new text
test = ["free cash", "meet me now"]
X_test = vectorizer.transform(test)
predictions = model.predict(X_test)

print("Predictions:", predictions)  # [1 0]
