import streamlit as st
import requests

# ------------------ Custom Page Config ------------------
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

# ------------------ Custom CSS Styling ------------------
st.markdown("""
    <style>
        .message-container {
            padding: 10px 20px;
            margin: 10px 0;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background-color: #DCF8C6;
            align-self: flex-end;
            margin-left: auto;
        }
        .bot-message {
            background-color: #F1F0F0;
            align-self: flex-start;
            margin-right: auto;
        }
        .chat-box {
            display: flex;
            flex-direction: column;
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ Page Title ------------------
st.markdown('<div class="title">🤖 Smart Chatbot</div>', unsafe_allow_html=True)

# ------------------ Chat History Init ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Input ------------------
query = st.text_input("💬 Write your question here", key="input", placeholder="Example: What is the best Linux distribution?")

# ------------------ Submit & Response ------------------
if query:
    url = "http://127.0.0.1:8000/llm/"
    payload = { "query": query }

    try:
        with requests.post(url, json=payload) as r:
            r.raise_for_status()
            response_data = r.json()
            bot_response = response_data.get("answer", "❗ No response.")

            # Append to chat history
            st.session_state.chat_history.append(("User", query))
            st.session_state.chat_history.append(("Bot", bot_response))
    except Exception as e:
        st.error(f"An error occurred: {e}")

# ------------------ Display Chat ------------------
for role, message in st.session_state.chat_history:
    if role == "User":
        st.markdown(f'<div class="message-container user-message chat-box">👤 {message}</div>', unsafe_allow_html=True)
    elif role == "Bot":
        st.markdown(f'<div class="message-container bot-message chat-box">🤖 {message}</div>', unsafe_allow_html=True)