from backend.processor import translate_text

def translate_custom_text(input_text: str, target_lang: str) -> str:
    """
    Translate any arbitrary text into the target language.
    
    Args:
        input_text (str): The text to translate.
        target_lang (str): The target language (e.g., 'Hindi', 'Spanish').
    
    Returns:
        str: Translated text or an error message if input is missing.
    """
    if not input_text:
        return "⚠️ Please enter some text to translate."
    
    try:
        return translate_text(input_text, target_lang)
    except Exception as e:
        return f"❌ Translation failed: {str(e)}"
