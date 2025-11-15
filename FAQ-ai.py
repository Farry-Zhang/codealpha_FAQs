import streamlit as st
import requests
import json

st.set_page_config(page_title="Purple AI Chatbot", page_icon="💜", layout="centered")

# ------------------- Purple Theme CSS -------------------
st.markdown("""
<style>

body {
    background: #f3e9ff;
}

.chat-container {
    max-height: 420px;
    overflow-y: auto;
    padding: 16px;
    border-radius: 14px;
    background: #f4efff;
    border: 2px solid #d3c1ff;
    box-shadow: 0 0 12px rgba(150, 90, 255, 0.15);
}

.user-msg {
    background: linear-gradient(135deg, #b78cff, #d7c3ff);
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 12px 0;
    text-align: right;
    font-size: 16px;
    box-shadow: 0 0 8px rgba(183, 140, 255, 0.35);
}

.bot-msg {
    background: white;
    color: #4a3b72;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 12px 0;
    border: 1px solid #d1c4ff;
    font-size: 16px;
    box-shadow: 0 0 6px rgba(130, 100, 200, 0.1);
}

/* 紫色输入框 */
input[type="text"] {
    border: 2px solid #bfa3ff !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* Purple title */
h1 {
    color: #7a35ff;
    text-align: center;
    font-weight: 800;
}

/* Purple label */
label {
    color: #6c2df7 !important;
    font-size: 18px !important;
}

/* Remove scrollbar ugliness */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-thumb {
    background: #c8afff;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ------------------- Ollama 调用 -------------------
def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {"model": "llama3.1", "prompt": prompt}

    response = requests.post(url, json=data, stream=True)
    full_text = ""

    for line in response.iter_lines():
        if line:
            obj = json.loads(line.decode())
            full_text += obj.get("response", "")

    return full_text


# ------------------- UI -------------------
st.title("💜 AI Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 聊天框
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="user-msg">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 输入框
user_input = st.text_input("💬 Your message:")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    answer = ask_ollama(user_input)
    st.session_state.chat_history.append(("bot", answer))
    st.rerun()
