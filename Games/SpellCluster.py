import random
import time

spells = {
    "lumos": "💡 Your surroundings glow with soft light.",
    "ignis": "🔥 A burst of fire shoots forward.",
    "aqua": "💧 Water flows from your fingertips.",
    "ventus": "🌪️ Wind swirls violently around you.",
    "tempus": "⏳ Time slows down momentarily.",
    "electra": "⚡ Lightning crackles in your palm.",
}

print("🔮 Welcome, Spell Caster!\nType a spell (e.g., 'ignis', 'ventus', etc.) or type 'exit'.\n")

while True:
    cmd = input("✨ Cast: ").lower()
    if cmd == "exit":
        print("🧙‍♂️ You vanish in a puff of smoke!")
        break
    effect = spells.get(cmd)
    if effect:
        print("💥 " + effect)
        time.sleep(1)
    else:
        print("❌ Nothing happens... Try a real spell.")
