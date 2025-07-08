import math
from collections import defaultdict

# Sample training data
data = [
    ("buy cheap pills", "spam"),
    ("cheap meds now", "spam"),
    ("hello friend", "ham"),
    ("how are you", "ham")
]

def train_naive_bayes(data):
    word_counts = {"spam": defaultdict(int), "ham": defaultdict(int)}
    class_counts = {"spam": 0, "ham": 0}
    total_words = {"spam": 0, "ham": 0}

    for text, label in data:
        class_counts[label] += 1
        for word in text.split():
            word_counts[label][word] += 1
            total_words[label] += 1

    vocab = set(word for label in word_counts for word in word_counts[label])
    return word_counts, class_counts, total_words, vocab

def predict(text, word_counts, class_counts, total_words, vocab):
    results = {}
    for label in ["spam", "ham"]:
        log_prob = math.log(class_counts[label] / sum(class_counts.values()))
        for word in text.split():
            word_freq = word_counts[label].get(word, 0) + 1
            word_prob = word_freq / (total_words[label] + len(vocab))
            log_prob += math.log(word_prob)
        results[label] = log_prob
    return max(results, key=results.get)

# Train
word_counts, class_counts, total_words, vocab = train_naive_bayes(data)

# Predict
test_text = "cheap pills now"
print(f"Prediction for '{test_text}':", predict(test_text, word_counts, class_counts, total_words, vocab))
