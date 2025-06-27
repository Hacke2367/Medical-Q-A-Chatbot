# 🩺 Multilingual Medical Q&A Chatbot

A specialized medical question-answering chatbot built using the [MedQuAD dataset](https://github.com/abachaa/MedQuAD), capable of understanding and responding to user queries in **English**, **Spanish**, **Hindi**, and **French**.

This project was developed in **two major phases**:

---

## ✅ Phase 1: Medical Q&A Chatbot using MedQuAD Dataset

- Built a domain-specific chatbot using the curated MedQuAD dataset containing thousands of medical questions and answers from trusted health sources like NIH.
- Implemented a **TF-IDF-based retrieval mechanism** to identify the most relevant medical answer based on user queries.
- Cleaned and normalized medical questions for better matching using `scikit-learn`, `regex`, and domain-aware preprocessing.
- Designed a simple yet functional frontend using **Streamlit** for users to ask questions and receive direct medical responses.
- Added basic recognition of medical entities such as symptoms, diseases, and treatments to ensure context-aware results.

---

## 🌍 Phase 2: Multilingual Support & Advanced Processing

- Extended the chatbot to support **four languages**: `English (en)`, `Spanish (es)`, `Hindi (hi)`, and `French (fr)`.
- Integrated **automatic language detection** using `langdetect`, enhanced with domain-specific medical keywords for accuracy.
- Implemented **dynamic translation pipeline** using `deep-translator` to:
  - Translate non-English queries to English before retrieval
  - Translate English answers back to the user's original language for a seamless experience
- Added **long-text translation chunking** support to avoid API limitations and ensure full answer translation.
- Enabled **real-time question processing and streaming UI** via Streamlit with session memory.


## 🛠️ Tech Stack

- **Backend & NLP:** Python, Pandas, scikit-learn, TF-IDF, cosine similarity
- **Language Support:** langdetect, deep-translator (GoogleTranslator)
- **Frontend:** Streamlit
- **Data Source:** [MedQuAD dataset](https://github.com/abachaa/MedQuAD)

---

## 🚀 Features

- 🔍 Accurate retrieval from 15,000+ curated Q&A pairs
- 🌐 Multilingual Q&A (English, Spanish, Hindi, French)
- 🧠 Smart medical question preprocessing
- 🗨️ Streamlit-powered interactive UI
- 📦 Model saving/loading with pickle for fast reloads
- ✅ Fallback handling for unsupported or vague queries

---

## 🧪 Sample Questions to Try

| Language | Sample Query |
|---------|--------------|
| English | What are the symptoms of diabetes? |
| Spanish | ¿Cuáles son los síntomas del cáncer de pulmón? |
| Hindi   | उच्च रक्तचाप के लक्षण क्या हैं? |
| French  | Quels sont les symptômes de l'hypertension artérielle? |

---

## 📁 Folder Structure

```
MEDICAL_CHAT_BOT/
│
├── data/
│   └── processed_medquad_qa.csv
├── model/
│   └── retrieval_model.pkl
├── src/
│   ├── retrieval_model.py
│   └── language_utils.py
├── streamlit_app.py
└── README.md
```

---

## 📌 Future Improvements

- Incorporate semantic search (e.g., Sentence Transformers + FAISS)
- Integrate speech-to-text for voice queries
- Expand support to more global languages
- Add user feedback collection for continuous improvement

---

## 🙌 Acknowledgements

- MedQuAD Dataset by the U.S. National Library of Medicine
- [deep-translator](https://github.com/nidhaloff/deep-translator)
- Streamlit for rapid UI prototyping

---

## 💡 Usage

1. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

2. Run the chatbot  
   ```bash
   streamlit run streamlit_app.py
   ```

3. Ask medical questions in any supported language!

---

> ❗ Disclaimer: This chatbot is for **informational purposes only** and does **not substitute professional medical advice**. Always consult a healthcare provider for serious concerns.
