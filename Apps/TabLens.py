import time
import re
import random
import pygetwindow as gw
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Simple training dataset (you can expand it)
titles = [
    "ChatGPT - OpenAI", "YouTube - Music", "LinkedIn Jobs", "Python Multithreading", 
    "Netflix - Breaking Bad", "Instagram - Home", "GitHub Repositories", "Stack Overflow",
    "WhatsApp Web", "News - Ukraine Conflict", "Spotify - Top Hits"
]
labels = [
    "research", "entertainment", "work", "research",
    "entertainment", "social", "work", "research",
    "social", "news", "entertainment"
]

# Train classifier
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(titles)
clf = MultinomialNB()
clf.fit(X, labels)

# Scoring Map
scores = {"work": 30, "research": 35, "news": 15, "social": -10, "entertainment": -20}

# Get current active window title
def get_active_window_title():
    try:
        return gw.getActiveWindowTitle()
    except:
        return None

def predict_category(title):
    if not title:
        return "unknown", 0
    x = vectorizer.transform([title])
    label = clf.predict(x)[0]
    score = scores.get(label, 0)
    return label, score

def normalize_focus(total, count):
    return min(max(int(total / count + 50), 0), 100)  # Normalize to 0–100 scale

# Run loop
def main():
    print("Tracking browser activity. Press Ctrl+C to stop.\n")
    total_score = 0
    count = 0

    try:
        while True:
            title = get_active_window_title()
            if title:
                cat, score = predict_category(title)
                total_score += score
                count += 1
                focus = normalize_focus(total_score, count)
                print(f"[{time.strftime('%H:%M:%S')}] Tab: {title[:50]}...")
                print(f" → Category: {cat.upper()} | Score: {score} | Focus: {focus}%\n")
            time.sleep(5)  # Every 5 seconds
    except KeyboardInterrupt:
        print("\n[Session Ended]")

if __name__ == "__main__":
    main()
