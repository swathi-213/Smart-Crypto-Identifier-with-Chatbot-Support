# Cryptography Chatbot (Offline LLM)

This project implements a ChatGPT-like chatbot specialized in cryptography.

## Features
- Answers cryptography questions in natural language
- Covers symmetric, asymmetric, hash, stream ciphers
- Warns about broken and deprecated algorithms
- Works offline using a local LLM (Ollama)
- No API keys required

## Technologies
- Python
- Streamlit
- Ollama (LLaMA / Qwen)

## How to Run
1. Install Ollama
2. Pull model:
   ollama pull llama3.1
3. Install dependencies:
   pip install -r requirements.txt
4. Run:
   streamlit run app.py

## Academic Note
This chatbot is for educational purposes only and does not provide production cryptographic advice.