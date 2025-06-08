import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
        return recognizer.recognize_google(audio)
    except Exception as e:
        return f"Speech recognition error: {e}"
