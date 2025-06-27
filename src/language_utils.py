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

# first one

# from langdetect import detect, DetectorFactory
# from googletrans import Translator
# import re
#
# # Ensure consistent language detection
# DetectorFactory.seed = 0
#
# # Supported languages with cultural greetings
# SUPPORTED_LANGUAGES = {
#     'en': {'name': 'English', 'greeting': 'Hello! How can I assist with your medical questions?'},
#     'es': {'name': 'Spanish', 'greeting': '¡Hola! ¿Cómo puedo ayudarte con tus preguntas médicas?'},
#     'hi': {'name': 'Hindi', 'greeting': 'नमस्ते! मैं आपके चिकित्सा प्रश्नों में कैसे सहायता कर सकता हूँ?'},
#     'fr': {'name': 'French', 'greeting': 'Bonjour ! Comment puis-je vous aider avec vos questions médicales ?'}
# }
#
# # Medical terms in different languages
# MEDICAL_TERMS = {
#     'en': ["symptom", "treatment", "diagnosis", "disease", "medicine", "fever", "pain", "blood pressure",
#            "high blood pressure", "hypertension"],
#     'es': ["síntoma", "tratamiento", "diagnóstico", "enfermedad", "medicina", "fiebre", "dolor", "presión arterial",
#            "presión arterial alta", "hipertensión"],
#     'hi': ["लक्षण", "उपचार", "निदान", "रोग", "दवा", "बुखार", "दर्द", "रक्तचाप", "उच्च रक्तचाप", "हाइपरटेंशन"],
#     'fr': ["symptôme", "traitement", "diagnostic", "maladie", "médecine", "fièvre", "douleur", "pression artérielle",
#            "hypertension artérielle", "hypertension"]
# }
#
# # Hindi medical term mappings
# HINDI_MEDICAL_MAP = {
#     "high blood pressure": "उच्च रक्तचाप",
#     "hypertension": "उच्च रक्तचाप",
#     "symptoms": "लक्षण",
#     "fever": "बुखार",
#     "headache": "सिरदर्द",
#     "diabetes": "मधुमेह",
#     "heart disease": "हृदय रोग"
# }
#
#
# class LanguageProcessor:
#     def __init__(self):
#         self.translator = Translator()
#         self.target_lang = 'en'
#
#     def detect_language(self, text):
#         """Detect language with medical term enhancement"""
#         if not text.strip():
#             return 'en'
#
#         try:
#             # First try standard detection
#             lang = detect(text)
#
#             # Enhance with medical term matching
#             for code, terms in MEDICAL_TERMS.items():
#                 if any(term in text.lower() for term in terms):
#                     return code
#
#             return lang if lang in SUPPORTED_LANGUAGES else 'en'
#         except:
#             return 'en'
#
#     def translate_medical(self, text, src, dest):
#         """Specialized medical translation"""
#         try:
#             # First try standard translation
#             translation = self.translator.translate(text, src=src, dest=dest)
#             translated_text = translation.text
#
#             # Special handling for Hindi
#             if dest == 'hi':
#                 # Apply custom medical mappings
#                 for eng_term, hindi_term in HINDI_MEDICAL_MAP.items():
#                     translated_text = translated_text.replace(eng_term, hindi_term)
#
#                 # Fix common translation errors
#                 translated_text = translated_text.replace("रक्त दबाव", "रक्तचाप")
#                 translated_text = translated_text.replace("लक्षणों", "लक्षण")
#                 translated_text = translated_text.replace("चिकित्सा स्थिति", "रोग")
#
#             return translated_text
#         except:
#             return text
#
#     def translate_to_english(self, text):
#         """Translate input to English for processing"""
#         if not text.strip():
#             return text
#
#         detected_lang = self.detect_language(text)
#         if detected_lang == 'en':
#             return text
#
#         # Special handling for Hindi to English
#         if detected_lang == 'hi':
#             # Apply reverse mappings
#             for hindi_term, eng_term in HINDI_MEDICAL_MAP.items():
#                 text = text.replace(hindi_term, eng_term)
#
#         return self.translate_medical(text, detected_lang, 'en')
#
#     def translate_to_target(self, text, target_lang):
#         """Translate output to target language"""
#         if not text.strip() or target_lang == 'en':
#             return text
#
#         return self.translate_medical(text, 'en', target_lang)
#
#     def get_cultural_response(self, key, lang='en'):
#         """Get culturally appropriate response"""
#         responses = {
#             'no_answer': {
#                 'en': "I couldn't find a precise medical answer. Try rephrasing with more details.",
#                 'es': "No encontré una respuesta médica precisa. Intente reformular con más detalles.",
#                 'hi': "मुझे सटीक चिकित्सा उत्तर नहीं मिला। कृपया अधिक विवरण के साथ पुनः प्रयास करें।",
#                 'fr': "Je n'ai pas trouvé de réponse médicale précise. Essayez de reformuler avec plus de détails."
#             },
#             'disclaimer': {
#                 'en': "This information is for educational purposes only. Consult a healthcare professional for medical advice.",
#                 'es': "Esta información es solo para fines educativos. Consulte a un profesional de la salud para obtener asesoramiento médico.",
#                 'hi': "यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। चिकित्सा सलाह के लिए किसी स्वास्थ्य पेशेवर से परामर्श लें।",
#                 'fr': "Ces informations sont fournies à titre éducatif uniquement. Consultez un professionnel de santé pour des conseils médicaux."
#             }
#         }
#         return responses.get(key, {}).get(lang, responses[key]['en'])
#
#     def get_greeting(self, lang='en'):
#         """Get language-specific greeting"""
#         return SUPPORTED_LANGUAGES.get(lang, SUPPORTED_LANGUAGES['en'])['greeting']



# 2nd one

# from langdetect import detect, DetectorFactory
# from googletrans import Translator
#
# # Ensure consistent language detection
# DetectorFactory.seed = 0
#
# # Supported languages with cultural greetings
# SUPPORTED_LANGUAGES = {
#     'en': {'name': 'English', 'greeting': 'Hello! How can I assist with your medical questions?'},
#     'es': {'name': 'Spanish', 'greeting': '¡Hola! ¿Cómo puedo ayudarte con tus preguntas médicas?'},
#     'hi': {'name': 'Hindi', 'greeting': 'नमस्ते! मैं आपके चिकित्सा प्रश्नों में कैसे सहायता कर सकता हूँ?'},
#     'fr': {'name': 'French', 'greeting': 'Bonjour ! Comment puis-je vous aider avec vos questions médicales ?'}
# }
#
# # Flag icons for each language
# LANGUAGE_FLAGS = {
#     'en': '🇺🇸',
#     'es': '🇪🇸',
#     'hi': '🇮🇳',
#     'fr': '🇫🇷'
# }
#
# # Culturally appropriate responses
# CULTURAL_RESPONSES = {
#     'en': {
#         'no_answer': "I couldn't find a precise medical answer. Try rephrasing with more details.",
#         'disclaimer': "This information is for educational purposes only. Consult a healthcare professional for medical advice."
#     },
#     'es': {
#         'no_answer': "No pude encontrar una respuesta médica precisa. Intente reformular con más detalles.",
#         'disclaimer': "Esta información es solo para fines educativos. Consulte a un profesional de la salud para obtener asesoramiento médico."
#     },
#     'hi': {
#         'no_answer': "मुझे कोई सटीक चिकित्सा उत्तर नहीं मिला। अधिक विवरण के साथ पुनः प्रयास करें।",
#         'disclaimer': "यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। चिकित्सा सलाह के लिए किसी स्वास्थ्य पेशेवर से परामर्श लें।"
#     },
#     'fr': {
#         'no_answer': "Je n'ai pas trouvé de réponse médicale précise. Essayez de reformuler avec plus de détails.",
#         'disclaimer': "Ces informations sont fournies à titre éducatif uniquement. Consultez un professionnel de santé pour des conseils médicaux."
#     }
# }
#
#
# class LanguageProcessor:
#     def __init__(self):
#         self.translator = Translator()
#         self.target_lang = 'en'
#
#     def detect_language(self, text):
#         """Detect language with fallback to English"""
#         if not text.strip():
#             return 'en'
#
#         try:
#             lang = detect(text)
#             # Normalize language codes
#             if lang in ['zh-cn', 'zh-tw']:
#                 lang = 'zh'
#             return lang if lang in SUPPORTED_LANGUAGES else 'en'
#         except:
#             return 'en'
#
#     def translate_to_english(self, text):
#         """Translate input to English for processing"""
#         if not text.strip():
#             return text
#
#         detected_lang = self.detect_language(text)
#         if detected_lang == 'en':
#             return text
#
#         try:
#             translation = self.translator.translate(text, dest='en', src=detected_lang)
#             return translation.text
#         except:
#             return text
#
#     def translate_to_target(self, text, target_lang):
#
#         if not text.strip() or target_lang == 'en':
#             return text
#
#
#         try:
#             translation = self.translator.translate(text, dest=target_lang, src='en')
#             return translation.text
#         except:
#             return text
#
#     def get_cultural_response(self, key, lang='en'):
#         """Get culturally appropriate response"""
#         return CULTURAL_RESPONSES.get(lang, CULTURAL_RESPONSES['en']).get(key, "")
#
#     def get_greeting(self, lang='en'):
#         """Get language-specific greeting"""
#         return SUPPORTED_LANGUAGES.get(lang, SUPPORTED_LANGUAGES['en'])['greeting']
#
#     def get_language_name(self, lang_code):
#         """Get full language name from code"""
#         return SUPPORTED_LANGUAGES.get(lang_code, {'name': 'English'})['name']