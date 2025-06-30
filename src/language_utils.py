import re
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

# Seed for consistent langdetect results
DetectorFactory.seed = 0

# Define supported languages
SUPPORTED_LANGUAGES = ['en', 'es', 'hi', 'fr']

# Language-specific medical terms for fallback detection
MEDICAL_TERMS = {
    'en': ["symptom", "treatment", "diagnosis", "disease", "medicine",
           "fever", "pain", "blood pressure", "hypertension", "diabetes"],
    'es': ["síntoma", "tratamiento", "diagnóstico", "enfermedad", "medicina",
           "fiebre", "dolor", "presión arterial", "hipertensión", "diabetes"],
    'hi': ["लक्षण", "उपचार", "निदान", "रोग", "दवा",
           "बुखार", "दर्द", "रक्तचाप", "उच्च रक्तचाप", "मधुमेह"],
    'fr': ["symptôme", "traitement", "diagnostic", "maladie", "médecine",
           "fièvre", "douleur", "pression artérielle", "hypertension", "diabète"]
}


def detect_language(text: str) -> str:
    """Detect language of the input text with fallback on medical keywords."""
    if not text.strip():
        return 'en'

    try:
        lang = detect(text)
        if lang in SUPPORTED_LANGUAGES:
            return lang
    except Exception as e:
        print(f"[Language Detection Error] {e}")

    # Fallback via keyword matching
    text_lower = text.lower()
    for lang_code, terms in MEDICAL_TERMS.items():
        if any(term in text_lower for term in terms):
            return lang_code

    return 'en'


def translate_text(text: str, source: str, target: str) -> str:
    """Translate text using GoogleTranslator with fail-safe fallback."""
    if source == target or not text.strip():
        return text

    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        print(f"[Translation] {source} ➜ {target}: {translated}")
        return translated
    except Exception as e:
        print(f"[Translation Error] Failed to translate from {source} to {target}: {e}")
        return text  # fallback: return original


def clean_text(text: str, lang: str = 'en') -> str:
    """Clean text language-specifically to retain alphabets, numerals and basic punctuation."""
    if not isinstance(text, str):
        return ""

    text = text.lower()
    if lang == 'hi':
        text = re.sub(r'[^\u0900-\u097F\s.]', '', text)  # Keep Devanagari chars
    else:
        text = re.sub(r'[^\w\s\.\-\'’]', '', text, flags=re.UNICODE)  # Keep accented Latin, dots, hyphens, apostrophes

    return re.sub(r'\s+', ' ', text).strip()

