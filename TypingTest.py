import time

test = "The quick brown fox jumps over the lazy dog."
print("Type this:\n", test)

input("Press Enter when ready...")
start = time.time()
typed = input(">>> ")
end = time.time()

speed = len(typed) / (end - start) * 60
accuracy = sum(1 for a, b in zip(typed, test) if a == b) / len(test) * 100

print(f"Speed: {speed:.2f} CPM")
print(f"Accuracy: {accuracy:.2f}%")
