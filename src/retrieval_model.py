import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re
import pickle
from pathlib import Path
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'es', 'hi', 'fr']

# Medical terms for language detection enhancement
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

class MedicalQARetrievalModel:
    def __init__(self, data_path="data/processed_medquad_qa.csv"):
        self.data_path = data_path
        self.df = None
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=50000,
            stop_words='english'
        )
        self.question_vector = None
        self.model_dir = "model"
        Path(self.model_dir).mkdir(exist_ok=True)
        self.translator = GoogleTranslator()

        self._load_data()
        self._build_vectorizer()

    def _load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        print(f"Loading data from {self.data_path} for retrieval model...")
        self.df = pd.read_csv(self.data_path)

        if self.df.empty:
            raise ValueError("Data file is empty")

        if 'lang' not in self.df.columns:
            self.df['lang'] = 'en'

        self.df['question_clean'] = self.df.apply(
            lambda row: self._clean_text(row['question'], row['lang']), axis=1
        )
        print(f"Loaded {len(self.df)} Q&A pairs.")

    def _clean_text(self, text, lang='en'):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        if lang == 'hi':
            text = re.sub(r'[^\u0900-\u097F\s.]', '', text)
        else:
            text = re.sub(r'[^\u0041-\u007A\u00C0-\u017F\s.]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _build_vectorizer(self):
        print("Building tf-idf vectorizer...")
        self.question_vector = self.vectorizer.fit_transform(self.df['question_clean'])
        print("TF-IDF vectorizer built successfully")

    def detect_language(self, text):
        if not text.strip():
            return 'en'
        try:
            lang = detect(text)
            if lang in SUPPORTED_LANGUAGES:
                return lang
            text_lower = text.lower()
            for lang_code, terms in MEDICAL_TERMS.items():
                if any(term in text_lower for term in terms):
                    return lang_code
        except Exception as e:
            print(f"Language detection error: {e}")
        return 'en'

    def translate_text(self, text, src, dest):
        """Translate long texts using deep_translator with chunking."""
        if src == dest or not text.strip():
            return text

        try:
            chunks = [text[i:i + 450] for i in range(0, len(text), 450)]
            translator = GoogleTranslator(source=src, target=dest)
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            final_translation = ' '.join(translated_chunks)
            print(f"Translated from {src} to {dest}: {final_translation}")
            return final_translation
        except Exception as e:
            print(f"Translation failed: {e}")
            return text


    def get_answer(self, user_query, top_k=1):
        user_lang = self.detect_language(user_query)
        print(f"Detected language: {user_lang}")

        en_query = self.translate_text(user_query, user_lang, 'en') if user_lang != 'en' else user_query
        print(f"Query (en): {en_query}")

        cleaned_query = self._clean_text(en_query, 'en')
        if not cleaned_query:
            fallback = "Please ask a valid medical question."
            return [{"answer": self.translate_text(fallback, 'en', user_lang), "similarity_score": 0.0}], user_lang

        query_vector = self.vectorizer.transform([cleaned_query])
        similarities = cosine_similarity(query_vector, self.question_vector).flatten()
        top_k_indices = similarities.argsort()[-top_k:][::-1]

        for idx in top_k_indices:
            score = similarities[idx]
            row = self.df.iloc[idx]

            # Ensure we only translate clean English answers
            if row['lang'] != 'en':
                continue  # skip non-English sources for better translations

            if score > 0.3:
                answer = row['answer']
                answer_translated = self.translate_text(answer, 'en', user_lang) if user_lang != 'en' else answer
                return [{"answer": answer_translated, "similarity_score": float(score)}], user_lang

        fallback = "I couldn't find a relevant answer. Try rephrasing."
        return [{"answer": self.translate_text(fallback, 'en', user_lang), "similarity_score": 0.0}], user_lang

    def save_model(self, path=None):
        if not path:
            path = os.path.join(self.model_dir, "retrieval_model.pkl")
        model_data = {
            'vectorizer': self.vectorizer,
            'question_vector': self.question_vector,
            'df': self.df
        }
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {path}")
        return path

    @classmethod
    def load_model(cls, path="model/retrieval_model.pkl"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        with open(path, 'rb') as f:
            model_data = pickle.load(f)

        model = cls.__new__(cls)
        model.vectorizer = model_data['vectorizer']
        model.question_vector = model_data['question_vector']
        model.df = model_data['df']
        model.model_dir = os.path.dirname(path)
        model.translator = GoogleTranslator()

        print(f"Model loaded from {path}")
        return model

# For testing
if __name__ == "__main__":
    model = MedicalQARetrievalModel()
    queries = [
        "what are symptoms of diabetes",                    # English
        "cuáles son los síntomas de la diabetes",           # Spanish
        "मधुमेह के लक्षण क्या हैं",                         # Hindi
        "quels sont les symptômes du diabète",             # French
        "कैंसर के लक्षण क्या हैं"                          # Hindi (test fallback)
    ]
    for q in queries:
        res, lang = model.get_answer(q)
        print(f"\nQuery ({lang}): {q}")
        print(f"✅ Answer: {res[0]['answer']}")
        print(f"Similarity Score: {res[0]['similarity_score']}")

