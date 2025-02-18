import deepspeech
import numpy as np
import wave
import io

# Cargar el modelo DeepSpeech
model_file_path = 'deepspeech-0.9.3-models.pbmm'
scorer_file_path = 'deepspeech-0.9.3-models.scorer'
model = deepspeech.Model(model_file_path)
model.enableExternalScorer(scorer_file_path)

def transcribe_audio_stream(audio_data):
    # Convertir los datos de audio a un formato que DeepSpeech pueda procesar
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    audio_array = audio_array.astype(np.float32) / 32768.0  # Normalizar el audio

    # Transcribir el audio
    text = model.stt(audio_array)
    return text
