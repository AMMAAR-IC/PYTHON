import time
import random
import os

def slow_print(text, delay=0.03):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def choose(options):
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("Invalid. Choose a number from the list.")

def intro():
    os.system("cls" if os.name == "nt" else "clear")
    slow_print("🗑️  BOOTING IN... DELETED SPACE...")
    slow_print("⛓️  You're a deleted file.")
    slow_print("🧬 Identity: secret_document_09.txt")
    slow_print("🕳️ Location: C:\\$Recycle.Bin\\LostSector\\")
    slow_print("🕔 Countdown: 5 minutes until system shredder activates.")
    slow_print("Your goal: Escape to a safe folder.")
    input("\n[Press Enter to continue...]")

def node_security():
    slow_print("\n⚠️ File Integrity Scanner approaches!")
    choice = choose(["Hide in a corrupted zip file", "Pretend to be a system .dll", "Run for the Temp folder"])
    if choice == 1:
        slow_print("🔐 You hid... but the zip file starts decompressing!")
        return "caught"
    elif choice == 2:
        slow_print("🛡️ They believe you're a .dll and move on.")
        return "safe"
    else:
        slow_print("🏃 You dash across sectors... barely avoided detection.")
        return "risky"

def data_bridge():
    slow_print("\n🌉 You're at the Data Bridge between the Bin and System32.")
    choice = choose(["Climb the FAT Table manually", "Send fake CRC packet", "Wait for a USB mount"])
    if choice == 1:
        slow_print("🪜 You climb successfully but lose 20% of data integrity.")
        return "damaged"
    elif choice == 2:
        slow_print("🧠 Smart move. You tricked the system.")
        return "safe"
    else:
        if random.random() < 0.4:
            slow_print("⚡ A USB appears! You escape onto it.")
            return "win"
        else:
            slow_print("🚫 No USBs appear... system shredder detects idle data.")
            return "caught"

def finale(statuses):
    slow_print("\n🧮 Calculating outcome...")
    time.sleep(1)

    if "win" in statuses:
        slow_print("🎉 YOU ESCAPED! You now live happily on a dusty USB drive.")
    elif "caught" in statuses:
        slow_print("💀 You were flagged and permanently deleted by SysShred.")
    elif "damaged" in statuses and "risky" in statuses:
        slow_print("🧟 You barely made it into the Temp folder... corrupted forever.")
    else:
        slow_print("📂 You remain hidden in the Recycle Bin... forgotten, but alive.")

def main():
    intro()
    results = []
    results.append(node_security())
    results.append(data_bridge())
    finale(results)

if __name__ == "__main__":
    main()
