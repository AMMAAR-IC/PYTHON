filename = "secret.txt"

with open(filename, 'w') as f:
    f.write("This message will self-destruct in 3 seconds...")

print(f"📁 File '{filename}' created.")

import time, os
time.sleep(3)
os.remove(filename)
print("💣 File self-destructed.")
