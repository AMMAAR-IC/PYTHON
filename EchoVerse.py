import speech_recognition as sr
from textblob import TextBlob
import datetime
import os

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now (press Ctrl+C to stop)...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except:
        print("❌ Couldn't understand audio.")
        return ""

def analyze(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    mood = "Positive" if polarity > 0.2 else "Negative" if polarity < -0.2 else "Neutral"
    keywords = list(set(blob.noun_phrases))
    return polarity, mood, keywords

def reflect(text, mood, keywords):
    reflection = f"Today, you expressed a {mood.lower()} mood. You talked about: {', '.join(keywords[:4])}. "
    if mood == "Positive":
        reflection += "Keep up the good energy! 💪"
    elif mood == "Negative":
        reflection += "It’s okay to feel low. Be kind to yourself. 🧠"
    else:
        reflection += "Stay balanced and keep reflecting. ☯️"
    return reflection

def save_entry(text, mood, reflection):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"journal_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, "a") as f:
        f.write(f"\n[{date}]\n")
        f.write(f"Entry: {text}\n")
        f.write(f"Mood: {mood}\n")
        f.write(f"Reflection: {reflection}\n")
    print(f"📔 Entry saved to {filename}")

def main():
    while True:
        try:
            text = listen()
            if not text:
                continue
            polarity, mood, keywords = analyze(text)
            reflection = reflect(text, mood, keywords)
            print(f"\n🧠 Reflection: {reflection}\n")
            save_entry(text, mood, reflection)
        except KeyboardInterrupt:
            print("\n🛑 Exiting Journal.")
            break

if __name__ == "__main__":
    main() 
