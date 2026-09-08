import random
bones = ["Femur", "Skull", "Humerus", "Rib", "Tibia", "Ulna"]
symptoms = ["cracked", "shattered", "dislocated", "twisted", "fractured"]

input("🤕 Scan your virtual bones (press Enter)...")
print("\n🔬 Analyzing...")

for _ in range(3):
    print(".", end='', flush=True)
    time.sleep(1)

print("\n💀 Diagnosis:")
print(f"{random.choice(bones)} is {random.choice(symptoms)}!")
