import random
import time

# Define activity types with base durations (in minutes)
activities = [
    {"name": "Studying", "duration": 60, "mood": "focused"},
    {"name": "Gaming", "duration": 90, "mood": "excited"},
    {"name": "Waiting in line", "duration": 15, "mood": "bored"},
    {"name": "Meditating", "duration": 30, "mood": "calm"},
    {"name": "Dreaming", "duration": 10, "mood": "surreal"},
    {"name": "Exams", "duration": 45, "mood": "anxious"},
    {"name": "Socializing", "duration": 50, "mood": "happy"},
]

# Perceived time multipliers based on mood
mood_multiplier = {
    "focused": 0.9,
    "excited": 0.6,
    "bored": 2.5,
    "calm": 1.0,
    "surreal": 0.2,
    "anxious": 1.8,
    "happy": 0.7
}

def simulate_day():
    print("🧠 TimeQuanta – AI Perception of Time Simulator\n")
    total_actual = 0
    total_perceived = 0

    for i in range(5):  # Simulate 5 events
        activity = random.choice(activities)
        actual = activity["duration"]
        perceived = round(actual * mood_multiplier[activity["mood"]], 2)

        total_actual += actual
        total_perceived += perceived

        print(f"▶️ {activity['name']} ({activity['mood']})")
        print(f"   - Actual time: {actual} min")
        print(f"   - Perceived time: {perceived} min\n")
        time.sleep(1)

    print("⏳ Summary:")
    print(f"   Total Actual Time: {total_actual} min")
    print(f"   Total Perceived Time: {round(total_perceived, 2)} min")
    print(f"   Day felt {round((total_perceived / total_actual) * 100, 1)}% as long.\n")

    if total_perceived < total_actual * 0.6:
        print("🌀 You had a fast, joyful day.")
    elif total_perceived > total_actual * 1.4:
        print("🐢 Time dragged today. Boredom dominated.")
    else:
        print("⚖️ Balanced experience. Neither too fast nor slow.")

if __name__ == "__main__":
    simulate_day()
