import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = Path(__file__).with_name("pet_state.json")
MAX_STAT   = 100
DECAY_PER_HOUR = {"hunger": 5, "happiness": 2, "energy": 3}

ASCII_PET = r"""
   (\_/)
   (•_•)
  / >🍪   {msg}
"""

def clamp(x, lo=0, hi=MAX_STAT):
    return max(lo, min(x, hi))

def load_state():
    if STATE_FILE.exists():
        with STATE_FILE.open() as f:
            data = json.load(f)
            data["last_seen"] = datetime.fromisoformat(data["last_seen"])
            return data
    # create a newborn
    return {
        "name": "Pixel‑Bunny",
        "birthday": datetime.now().isoformat(timespec="seconds"),
        "age_hours": 0,
        "hunger": 30,
        "happiness": 70,
        "energy": 80,
        "last_seen": datetime.now(),
        "runaway": False,
    }

def save_state(state):
    s = state.copy()
    s["last_seen"] = datetime.now().isoformat(timespec="seconds")
    with STATE_FILE.open("w") as f:
        json.dump(s, f, indent=2)

def advance_time(state):
    """Update stats based on time passed since last run."""
    now = datetime.now()
    hours = max(int((now - state["last_seen"]).total_seconds() // 3600), 0)
    state["age_hours"] += hours
    for stat, decay in DECAY_PER_HOUR.items():
        state[stat] = clamp(state[stat] - decay * hours)

    # check runaway condition
    if state["hunger"] == 0 or state["happiness"] == 0 or state["energy"] == 0:
        state["runaway"] = True

def show_pet(state, msg=""):
    os.system("cls" if os.name == "nt" else "clear")
    status_bar = (
        f"Hunger: {state['hunger']:3}  "
        f"Happy: {state['happiness']:3}  "
        f"Energy: {state['energy']:3}  "
        f"Age: {state['age_hours'] // 24}d{state['age_hours'] % 24}h"
    )
    print(ASCII_PET.format(msg=msg).rstrip("\n"))
    print(status_bar)
    print("\nCommands: feed | play | sleep | stats | exit")

def main():
    state = load_state()
    advance_time(state)

    if state["runaway"]:
        print("💔 Your pet has run away… Try taking better care next time!")
        STATE_FILE.unlink(missing_ok=True)
        return

    greeting = "Yay, good to see you!" if state["age_hours"] else "Hello, human!"
    show_pet(state, greeting)

    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "feed":
            state["hunger"] = clamp(state["hunger"] + 30)
            show_pet(state, "Nom nom nom!")
        elif cmd == "play":
            state["happiness"] = clamp(state["happiness"] + 25)
            state["energy"] = clamp(state["energy"] - 15)
            show_pet(state, "Wheee!")
        elif cmd == "sleep":
            print("😴 Zzz… (5 sec)")
            time.sleep(5)
            state["energy"] = clamp(state["energy"] + 40)
            show_pet(state, "All rested!")
        elif cmd == "stats":
            print(json.dumps({k: v for k, v in state.items() if k != "last_seen"}, indent=2))
        elif cmd == "exit":
            save_state(state)
            print("Pet saved. Bye!")
            break
        else:
            print("Unknown command. Try again.")

if __name__ == "__main__":
    main()
