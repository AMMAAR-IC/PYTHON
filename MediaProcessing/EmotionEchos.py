import time
from textblob import TextBlob
from colorama import Fore, Style
import random

def emotion_react(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0.5:
        emotion = "Joy 😊"
        color = Fore.GREEN
        beats = "💚💚💚"
    elif sentiment < -0.5:
        emotion = "Sadness 😢"
        color = Fore.BLUE
        beats = "💔💔💔"
    else:
        emotion = "Neutral 😐"
        color = Fore.YELLOW
        beats = "💛🖤💛"

    print(color + f"\nEmotion: {emotion}")
    print("Heartbeat:", end=" ", flush=True)
    for i in range(3):
        print(beats[i], end=" ", flush=True)
        time.sleep(0.5)
    print(Style.RESET_ALL)

text = input("Type your current thought: ")
emotion_react(text)
