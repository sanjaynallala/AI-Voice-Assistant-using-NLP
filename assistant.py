import warnings
warnings.filterwarnings("ignore")

import whisper
import pyttsx3
import sounddevice as sd
import scipy.io.wavfile as wav
import wikipedia
import datetime

# 🔊 Speak function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del engine

# 🎤 Record function
def record_audio(filename="audio.wav", seconds=5, fs=44100):
    print("Recording... Speak now!")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    wav.write(filename, fs, recording)
    print("Recording saved.")

# -------------------------

print("Loading Whisper...")
whisper_model = whisper.load_model("base")

# 🎤 Record fresh audio
record_audio()

print("Transcribing...")
result = whisper_model.transcribe("audio.wav", fp16=False)
user_text = result["text"].strip().lower()

print("\n🧑 You said:", user_text)

# -------------------------
# 🧠 Hybrid Logic
# -------------------------

response = ""

try:
    # 🔹 Rule-based responses
    if "time" in user_text:
        current_time = datetime.datetime.now().strftime("%H:%M")
        response = "The current time is " + current_time

    elif "date" in user_text:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        response = "Today's date is " + today

    elif "hello" in user_text:
        response = "Hello Sanjay! How can I help you?"

    # 🔹 If question → use Wikipedia
    else:
        print("Searching Wikipedia...")
        summary = wikipedia.summary(user_text, sentences=2)
        response = summary

except Exception:
    response = "Sorry, I could not find information about that."

print("🤖 Assistant:", response)

# 🔊 Speak response
speak(response)
