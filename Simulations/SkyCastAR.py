import random
import time
from datetime import datetime

weather_states = ["Clear", "Cloudy", "Rain", "Storm", "Fog", "Snow"]
wind_directions = ["North", "South", "East", "West", "North-East", "South-West"]

def generate_weather():
    temp = round(random.uniform(-5, 42), 1)  # Celsius
    humidity = random.randint(10, 100)
    pressure = random.randint(980, 1050)     # hPa
    wind_speed = round(random.uniform(0, 25), 1)
    wind_dir = random.choice(wind_directions)
    condition = random.choices(
        weather_states,
        weights=[20, 30, 20, 10, 10, 10],
        k=1
    )[0]
    return {
        "temperature": temp,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "wind_direction": wind_dir,
        "condition": condition
    }

def narrate(weather):
    mood = "pleasant"
    if weather['condition'] in ["Storm", "Rain", "Fog"]:
        mood = "moody"
    elif weather['temperature'] < 5:
        mood = "chilly"
    elif weather['temperature'] > 35:
        mood = "hot and intense"
    
    time_desc = "morning" if datetime.now().hour < 12 else "evening" if datetime.now().hour < 18 else "night"
    desc = f"""
🌤️  {datetime.now().strftime('%A, %H:%M')} ({time_desc.capitalize()})
Weather Report:
- Sky: {weather['condition']}
- Temperature: {weather['temperature']}°C
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} km/h blowing from {weather['wind_direction']}
- Pressure: {weather['pressure']} hPa

🧠 Mood: The weather feels {mood}.
"""
    return desc

def main():
    print("🛰️ SkyCastAR – Offline AI Weather Simulator\n")
    try:
        while True:
            weather = generate_weather()
            report = narrate(weather)
            print(report)
            time.sleep(10)  # Update every 10 sec
    except KeyboardInterrupt:
        print("\n[Session Ended]")

if __name__ == "__main__":
    main()
