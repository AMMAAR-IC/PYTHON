import random
import time
import os

FOLDERS = [
    r"C:\Photos\HappyMoments",
    r"C:\Code\ML_Project",
    r"C:\School\Final_Submission",
    r"D:\Games\SavedData",
    r"C:\System32",
]

VIRUSES = [
    "WORM.AI-1337",
    "DESTRUCTO.EXE",
    "MEME.TROJAN.9000",
    "RANSOM.MP4",
    "VIRAL_RICKROLL"
]

ACTIONS = ["SCAN", "QUARANTINE", "DELETE", "IGNORE"]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def type_out(msg, delay=0.02):
    for c in msg:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def virus_attack(folder, virus):
    clear()
    print("🚨 ALERT! FILE INFECTION DETECTED 🚨")
    print(f"📂 Target: {folder}")
    print(f"🦠 Virus: {virus}")
    print("🛡️  Available Actions:")
    for i, act in enumerate(ACTIONS, 1):
        print(f"{i}. {act}")
    return virus

def evaluate_response(choice, correct_action):
    if ACTIONS[choice - 1] == correct_action:
        type_out("✅ Virus successfully neutralized!")
        return True
    else:
        type_out("❌ Wrong action! Folder was compromised...")
        return False

def main():
    score = 0
    health = 3
    type_out("🛡️ Terminal Virus Defense Booting...\n")
    time.sleep(1)

    while health > 0:
        folder = random.choice(FOLDERS)
        virus = random.choice(VIRUSES)
        correct_action = random.choice(ACTIONS)

        virus_attack(folder, virus)

        try:
            choice = int(input("Select action (1-4): ").strip())
            if 1 <= choice <= 4:
                if evaluate_response(choice, correct_action):
                    score += 1
                else:
                    health -= 1
                    print(f"💔 System integrity: {health}/3")
            else:
                print("❓ Invalid choice! You lost time.")
                health -= 1
        except:
            print("⚠️ Input error! Lost time...")
            health -= 1
        time.sleep(2)

    print("\n🧨 SYSTEM BREACHED. FINAL SCORE:", score)
    print("Better luck next time, defender!")

if __name__ == "__main__":
    main()
