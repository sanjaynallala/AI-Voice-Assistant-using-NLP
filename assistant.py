import warnings
warnings.filterwarnings("ignore")

import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import wikipedia
import datetime
import time
import pyttsx3
import pythoncom   # IMPORTANT for Windows stability

# ==========================
# INITIAL SETUP
# ==========================

print("Loading Whisper model...")
model = whisper.load_model("base")

SAMPLE_RATE = 16000
DURATION = 5
AUDIO_FILE = "audio.wav"

# ==========================
# STABLE SPEAK FUNCTION
# ==========================

def speak(text):
    if not text or not text.strip():
        return

    print("🤖 Assistant:", text)

    try:
        pythoncom.CoInitialize()  # Fix Windows COM issue
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text[:600])
        engine.runAndWait()
        engine.stop()
        pythoncom.CoUninitialize()
    except Exception as e:
        print("TTS Error:", e)

# ==========================
# RECORD FUNCTION
# ==========================

def record_audio():
    print("\n🎤 Recording... Speak now!")

    recording = sd.rec(int(DURATION * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE,
                       channels=1,
                       dtype='float32')
    sd.wait()

    recording = np.squeeze(recording)
    recording = np.int16(recording * 32767)

    wav.write(AUDIO_FILE, SAMPLE_RATE, recording)
    print("✅ Recording complete.")

# ==========================
# TRANSCRIBE FUNCTION
# ==========================

def transcribe_audio():
    try:
        print("🔎 Transcribing...")
        result = model.transcribe(AUDIO_FILE, fp16=False)
        return result["text"].strip().lower()
    except Exception as e:
        print("Whisper Error:", e)
        return ""

# ==========================
# RESPONSE LOGIC
# ==========================

def generate_response(user_text):

    if not user_text:
        return "I did not hear anything clearly. Please try again."

    if any(word in user_text for word in ["exit", "quit", "stop"]):
        return "EXIT"

    if "time" in user_text:
        return "The current time is " + datetime.datetime.now().strftime("%I:%M %p")

    if "date" in user_text:
        return "Today's date is " + datetime.datetime.now().strftime("%B %d, %Y")

    if any(word in user_text for word in ["hello", "hi", "hey"]):
        return "Hello Sanjay! How can I help you?"

    try:
        print("🌐 Searching Wikipedia...")
        return wikipedia.summary(user_text, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "Your query is ambiguous. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "I could not find information about that."
    except Exception:
        return "Something went wrong while searching."

# ==========================
# MAIN LOOP
# ==========================

print("\n🎙 Hybrid AI Voice Assistant Started!")
print("Say 'exit' to stop.\n")

while True:
    record_audio()
    user_input = transcribe_audio()

    print("🧑 You said:", user_input)

    response = generate_response(user_input)

    if response == "EXIT":
        speak("Goodbye! Have a great day.")
        break

    speak(response)
    time.sleep(0.5)

print("Assistant stopped.")
