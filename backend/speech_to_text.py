import speech_recognition as sr
import io

def transcribe_audio_stream(audio_data):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, 16000, 2)  # Ajusta los parámetros según sea necesario
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        raise Exception(f"Could not request results from Google Speech Recognition service; {e}")
