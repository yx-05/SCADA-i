import pyttsx3

# 1. Initialize engine
engine = pyttsx3.init()

# 2. Adjust properties
engine.setProperty("rate", 150)     # speed of speech
engine.setProperty("volume", 1.0)   # max volume

# 3. Speak the text
engine.say("Hello! I am talking without the internet.")


