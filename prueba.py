import torch
import torchaudio
from transformers import AutoModelForCTC, AutoProcessor, MarianMTModel, MarianTokenizer

stt_model = AutoModelForCTC.from_pretrained("projecte-aina/stt-ca-citrinet-512")
processor = AutoProcessor.from_pretrained("projecte-aina/stt-ca-citrinet-512")

translator_model_name = "Helsinki-NLP/opus-mt-ca-es"
translator_tokenizer = MarianTokenizer.from_pretrained(translator_model_name)
translator_model = MarianMTModel.from_pretrained(translator_model_name)

def audio_to_text(audio_path):
    """Convierte un archivo de audio en texto usando STT en catalán."""
    waveform, sample_rate = torchaudio.load(audio_path)
    inputs = processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt")
    
    with torch.no_grad():
        logits = stt_model(**inputs).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    return transcription

def translate_text(text):
    """Traduce texto de catalán a español."""
    inputs = translator_tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = translator_model.generate(**inputs)
    translated_text = translator_tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return translated_text


# Cambia el nombre del audio por el tuyo plis
audio_file = "audio_catalan.wav" 
catalan_text = audio_to_text(audio_file)
print(f"Texto en Catalán: {catalan_text}")

translated_text = translate_text(catalan_text)
print(f"Texto en Español: {translated_text}")
