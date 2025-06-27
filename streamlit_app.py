import streamlit as st
from src.retrieval_model import MedicalQARetrievalModel

# --- MUST be first ---
st.set_page_config(page_title="🩺 Medical Chatbot", layout="wide")

# --- Load the model once ---
@st.cache_resource
def load_model():
    return MedicalQARetrievalModel()

model = load_model()

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- UI Layout ---
st.markdown("<h2 style='text-align: center;'>🩺 Multilingual Medical Chatbot</h2>", unsafe_allow_html=True)
st.caption("Ask your medical questions in **English, Hindi, Spanish, or French**. You'll get responses in the same language.")

# --- Input area ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your medical question here...", key="user_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    try:
        with st.spinner("Thinking..."):
            results, detected_lang = model.get_answer(user_input)
            top_answer = results[0]["answer"] if results else "Sorry, I couldn't find an answer."

        # Save to session state
        st.session_state.chat_history.append({
            "user": user_input,
            "bot": top_answer,
            "lang": detected_lang
        })

    except Exception as e:
        st.error(f"⚠️ Something went wrong: {e}")

# --- Chat Display ---
st.markdown("---")
st.subheader("💬 Chat History")

for i, chat in enumerate(reversed(st.session_state.chat_history)):
    with st.container():
        st.markdown(f"""
        <div style='background-color: #262730; color: #f5f5f5; padding: 12px 16px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #444;'>
            <strong>🧑 You:</strong><br>{chat['user']}
        </div>
        <div style='background-color: #1e1e1e; color: #d4f4dd; padding: 12px 16px; border-radius: 12px; margin-bottom: 16px; border: 1px solid #333;'>
            <strong>🤖 Bot:</strong><br>{chat['bot']}
        </div>
        """, unsafe_allow_html=True)


# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Built with ❤️ by Abhishek — powered by local AI.</p>", unsafe_allow_html=True)








##  ye complete medical chatbot ka code hai
#
# import streamlit as st
# import os
# from src.retrieval_model import MedicalQARetrievalModel
# from src.language_utils import SUPPORTED_LANGUAGES
#
# # --- Session Setup ---
# if 'model' not in st.session_state:
#     st.session_state.model = None
# if 'initialized' not in st.session_state:
#     st.session_state.initialized = False
# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'user_lang' not in st.session_state:
#     st.session_state.user_lang = 'en'
# if 'processing' not in st.session_state:
#     st.session_state.processing = False
#
# # --- Page Config ---
# st.set_page_config(
#     page_title="Medical Q&A Chatbot",
#     page_icon="🩺",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )
#
# # --- Custom CSS ---
# st.markdown("""
# <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
# <style>
# html, body, [class*="css"] {
#     font-family: 'Inter', sans-serif;
#     font-size: 16px;
# }
# .stApp {
#     background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
# }
# .user-message {
#     background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
#     color: white;
#     padding: 12px 18px;
#     border-radius: 20px 20px 0 20px;
#     margin: 10px 0;
#     max-width: 80%;
#     margin-left: auto;
#     box-shadow: 0 4px 8px rgba(0,0,0,0.1);
# }
# .bot-message {
#     background: #ffffff;
#     color: #333333;
#     padding: 12px 18px;
#     border-radius: 20px 20px 20px 0;
#     margin: 10px 0;
#     max-width: 80%;
#     box-shadow: 0 4px 8px rgba(0,0,0,0.05);
#     border: 1px solid #e0e0e0;
# }
# .header {
#     background: linear-gradient(90deg, #2196F3 0%, #21CBF3 100%);
#     color: white;
#     padding: 20px;
#     border-radius: 0 0 20px 20px;
#     margin-bottom: 30px;
#     box-shadow: 0 4px 12px rgba(0,0,0,0.1);
# }
# </style>
# """, unsafe_allow_html=True)
#
# # --- Header UI ---
# st.markdown("""
# <div class='header'>
#     <h1 style='margin:0;'>Medical Q&A Chatbot</h1>
#     <p style='margin:0; opacity:0.9'>Ask any health-related question</p>
# </div>
# """, unsafe_allow_html=True)
#
#
# # --- Load or Build Model ---
# def initialize_model():
#     try:
#         model_path = "model/retrieval_model.pkl"
#
#         # Show loading status
#         with st.spinner("🏥 Loading medical knowledge base..."):
#             if os.path.exists(model_path):
#                 st.session_state.model = MedicalQARetrievalModel.load_model(model_path)
#             else:
#                 st.session_state.model = MedicalQARetrievalModel(data_path="data/processed_medquad_qa.csv")
#                 st.session_state.model.save_model()
#
#             # Add initial greeting
#             if not st.session_state.messages:
#                 greeting = st.session_state.model.language_processor.get_greeting(st.session_state.user_lang)
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": greeting
#                 })
#
#             st.session_state.initialized = True
#
#     except Exception as e:
#         st.error(f"🚨 Initialization failed: {str(e)}")
#         st.stop()
#
#
# # --- Chat Flow ---
# def display_chat():
#     # Display chat history
#     for msg in st.session_state.messages:
#         role = msg["role"]
#         content = msg["content"]
#         if role == "user":
#             st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="bot-message">{content}</div>', unsafe_allow_html=True)
#
#     # Get placeholder based on language
#     placeholder_text = {
#         'en': "Ask a medical question...",
#         'es': "Haga una pregunta médica...",
#         'hi': "एक चिकित्सा प्रश्न पूछें...",
#         'fr': "Posez une question médicale..."
#     }.get(st.session_state.user_lang, "Ask a medical question...")
#
#     user_query = st.chat_input(placeholder_text)
#
#     if user_query and not st.session_state.processing:
#         st.session_state.messages.append({"role": "user", "content": user_query})
#         st.session_state.processing = True
#         st.rerun()
#
#
# # --- Process Query ---
# def process_query():
#     if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
#         user_query = st.session_state.messages[-1]["content"]
#         with st.spinner("🔍 Searching medical knowledge..."):
#             try:
#                 answers, detected_lang = st.session_state.model.get_answer(user_query, top_k=1)
#
#                 # Update language if detected different
#                 if detected_lang != st.session_state.user_lang:
#                     st.session_state.user_lang = detected_lang
#
#                 if answers and answers[0]['similarity_score'] > 0.15:
#                     reply = answers[0]['answer'].strip()
#                     st.session_state.messages.append({"role": "assistant", "content": reply})
#                 else:
#                     no_answer = st.session_state.model.language_processor.get_cultural_response(
#                         'no_answer',
#                         st.session_state.user_lang
#                     )
#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": f"⚠️ {no_answer}"
#                     })
#
#             except Exception as e:
#                 st.error(f"🚨 Error: {str(e)}")
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": "⚠️ Sorry, I encountered an error processing your request"
#                 })
#             finally:
#                 st.session_state.processing = False
#                 st.rerun()
#
#
# # --- Main App Flow ---
# if not st.session_state.initialized:
#     initialize_model()
#
# if st.session_state.initialized:
#     display_chat()
#     process_query()
#
# # --- Sidebar ---
# with st.sidebar:
#     if st.session_state.initialized:
#         st.subheader("🌐 Language Settings")
#
#         # Language selector
#         selected_lang = st.selectbox(
#             "Select your language:",
#             options=list(SUPPORTED_LANGUAGES.keys()),
#             format_func=lambda code: SUPPORTED_LANGUAGES[code]['name'],
#             index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.user_lang)
#         )
#
#         if selected_lang != st.session_state.user_lang:
#             st.session_state.user_lang = selected_lang
#             st.session_state.messages = [{
#                 "role": "assistant",
#                 "content": st.session_state.model.language_processor.get_greeting(selected_lang)
#             }]
#             st.rerun()
#
#         st.divider()
#
#     st.subheader("ℹ️ About")
#     st.markdown("""
#     - Powered by MedQuAD
#     - Supports English, Spanish, Hindi, French
#     - Automatic language detection
#     """)
#
#     if st.session_state.initialized:
#         # Culturally appropriate disclaimer
#         disclaimer = st.session_state.model.language_processor.get_cultural_response(
#             'disclaimer',
#             st.session_state.user_lang
#         )
#         st.markdown("### ⚠️ Disclaimer")
#         st.caption(disclaimer)
#
#     if st.button("🧹 Clear Chat", use_container_width=True):
#         st.session_state.messages = []
#         if st.session_state.initialized:
#             greeting = st.session_state.model.language_processor.get_greeting(st.session_state.user_lang)
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": greeting
#             })
#         st.rerun()
#
#
