import streamlit as st
from src.retrieval_model import MedicalQARetrievalModel

st.set_page_config(page_title="🩺 Medical Chatbot", layout="wide")

@st.cache_resource
def load_model():
    return MedicalQARetrievalModel()

model = load_model()

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


st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Built with ❤️ by Abhishek — powered by local AI.</p>", unsafe_allow_html=True)







