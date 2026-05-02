# app.py
import streamlit as st # type: ignore
from crypto_chatbot.intent import detect_intent
from crypto_chatbot.prompt_builder import build_system_prompt
from crypto_chatbot.local_llm import query_llm

st.set_page_config(
    page_title="Cryptography Chatbot",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
/* Completely hide sidebar */
[data-testid="stSidebar"] {
    display: none;
}

/* Remove the small arrow button */
[data-testid="collapsedControl"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #1e0b36, #0f0a1a 70%);
}

html, body, [class*="css"] {
    color: #e9d5ff;
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.block-container {
    max-width: 1000px;   /* 👈 minimum-wide feel */
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Reduce chat input width and center it */
div[data-testid="stChatInput"] {
    max-width: 1000px;   /* adjust: 900–1100px */
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)
st.title("🔐 CipherScope")
st.caption("Unified Cryptographic Security Analysis & Expert Chatbot")
nav1, nav2 = st.columns(2)

with nav1:
    if st.button("🔐 Cipher Analysis Engine", use_container_width=True):
        st.switch_page("app.py")

with nav2:
    if st.button("🧠 Crypto Chatbot", use_container_width=True):
        pass


st.title("🧠 Crypto Chatbot")
st.caption("Ask, Compare & Understand Cryptographic Algorithms")
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