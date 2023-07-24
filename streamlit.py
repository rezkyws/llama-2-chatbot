import streamlit as st
import requests

st.title("💬 Chatbot (based on Llama 2)")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    print(st.session_state.messages)
    response = requests.post('http://localhost:4342/chat', json={"text": st.session_state.messages}, timeout=60).json()
    response = {"choices": [{
        "message": {
            "role": "assistant",
            "content": response["result"]
        }
    }]}
    msg = response["choices"][0]["message"]
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])