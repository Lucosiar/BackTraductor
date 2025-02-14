from transformers import MarianMTModel, MarianTokenizer

# Cargar el modelo y el tokenizador para la traducción
model_name = 'Helsinki-NLP/opus-mt-es-en'  # Modelo de español a inglés
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_text(text: str, target_language: str) -> str:
    try:
        # Tokenizar el texto
        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        # Generar la traducción
        translated_tokens = model.generate(**tokens)
        # Decodificar la traducción
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")
