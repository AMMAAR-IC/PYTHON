import random
from collections import defaultdict

def build_chain(text, n=2):
    words = text.split()
    chain = defaultdict(list)
    for i in range(len(words) - n):
        key = tuple(words[i:i+n])
        chain[key].append(words[i+n])
    return chain

def generate_text(chain, n=2, length=50):
    key = random.choice(list(chain.keys()))
    output = list(key)
    for _ in range(length):
        next_word = random.choice(chain.get(key, ['']))
        output.append(next_word)
        key = tuple(output[-n:])
    return ' '.join(output)

# Example
sample_text = """
ChatGPT is a tool made to generate useful and interesting responses. 
It helps developers, students, and creators to build smart applications. 
Learning Python is fun and rewarding when you automate things creatively.
"""

chain = build_chain(sample_text)
print(generate_text(chain))
