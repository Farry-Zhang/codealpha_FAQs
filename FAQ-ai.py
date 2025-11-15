import streamlit as st
import requests
import json

def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.1",
        "prompt": prompt
    }

    response = requests.post(url, json=data, stream=True)

    full_text = ""
    for line in response.iter_lines():
        if line:
            obj = json.loads(line.decode())
            full_text += obj.get("response", "")

    return full_text


st.title("Chatbot")
st.write("Ask anything!")

user_input = st.text_input("You:")

if user_input:
    answer = ask_ollama(user_input)
    st.text_area("Chatbot:", value=answer, height=200)
