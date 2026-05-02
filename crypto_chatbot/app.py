# app.py
import streamlit as st
from intent import detect_intent
from prompt_builder import build_system_prompt
from local_llm import query_llm

st.set_page_config(page_title="Cryptography Chatbot", layout="centered")
st.title("🔐 Cryptography Chatbot")
st.caption("Free • Offline • Crypto-specialized")

# ---------------------------
# RESET BUTTON (TOP RIGHT)
# ---------------------------
col1, col2 = st.columns([8, 2])
with col2:
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------
# INIT SESSION STATE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# DISPLAY CHAT HISTORY
# ---------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------------------
# CHAT INPUT
# ---------------------------
user_input = st.chat_input("Ask anything about cryptography")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Add system prompt ONCE per session
    if not any(m["role"] == "system" for m in st.session_state.messages):
        intent = detect_intent(user_input)
        system_prompt = build_system_prompt(intent, user_input)
        st.session_state.messages.insert(
            0, {"role": "system", "content": system_prompt}
        )

    # Limit history for speed (current chat only)
    MAX_HISTORY = 6
    recent_messages = st.session_state.messages[-MAX_HISTORY:]

    # Query LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_llm(recent_messages)
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )