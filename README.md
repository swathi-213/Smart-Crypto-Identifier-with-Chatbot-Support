<<<<<<< HEAD
![Uploading algorithm detection and security analusis for strong algorithm.png…]()
=======
>>>>>>> 884f5f1 (Update README and add screenshots)
# CipherScope

A unified cryptography toolkit for security analysis, algorithm detection, secure re-encryption, and an expert chatbot.

## Overview

CipherScope is a Streamlit-based application that combines:

- **Cryptographic algorithm detection** from uploaded encrypted files
- **Usage-aware security analysis** for data at rest, transit, IoT, finance, healthcare, and more
- **Secure re-encryption guidance** for stronger algorithm choices
- **Offline crypto chatbot** powered by a local LLM through Ollama

This project is designed for academic demonstration and security learning, not as a production cryptography service.

## Key Features

- Detects cryptographic algorithm families and specific algorithms using machine learning ensembles
- Analyzes algorithm security by selected data usage
- Recommends stronger alternatives and supports secure re-encryption for applicable cases
- Offers a chatbot interface for cryptography questions, comparisons, and explanations
- Uses a local Ollama model for offline language generation

## Repository Structure

- `app.py` — Main Streamlit app for cryptographic analysis and re-encryption
- `pages/chatbot.py` — Streamlit chatbot page for cryptography Q&A
- `crypto_chatbot/` — Local chatbot logic
  - `local_llm.py` — Ollama request handler
  - `prompt_builder.py` — System prompt builder
  - `intent.py` — User intent detection
  - `crypto_data.py` — Crypto grounding facts
- `modules/` — Core feature extraction and ML modules
  - `module1_features.py` — Encrypted-file feature extraction
  - `module2_detection.py` — Algorithm detection ensemble
  - `module3_usage.py` — Usage taxonomy for security decisions
  - `module4_security.py` — Usage-based security policy rules
  - `module5_reencryption.py` — Secure re-encryption helpers
- `models/` — Saved model artifacts used by the analyzer
- `features_enhanced.csv` — Feature dataset for training the detection models
- `train.py` — Script to rebuild stage-1 and stage-2 detection models
- `requirements.txt` — Python dependencies

## Screenshots

### User interface

![CipherScope Home](output%20screenshots/UI.png)

### Algorithm detection and security analysis

![Algorithm Detection](output%20screenshots/Algorithm%20Detection.png)

### Chatbot interface

![Crypto Chatbot](output%20screenshots/chatbot%20ui.png)

### Secure re-encryption workflow

![Secure Re-Encryption](output%20screenshots/reencryption.png)

## Requirements

- Python 3.10+ (recommended)
- `venv` or any virtual environment
- Streamlit
- Requests
- NumPy, pandas, scikit-learn, XGBoost, joblib
- Optional: `cryptography` for re-encryption support
- Ollama installed locally for the chatbot

## Setup

1. Open a terminal in the project folder:

```powershell
cd /d "C:\Users\Swathi\Documents\Phase1 Final Year Project\project phase2"
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

4. Install Ollama and pull a model if you want to use the chatbot:

```powershell
ollama pull llama3.1
```

> If `llama3.1` is too large or slow to download, you may use another local Ollama model. If you do, update `crypto_chatbot/local_llm.py` to set `MODEL_NAME` to the installed model name.

## Running the App

### Start the main CipherScope analyzer

```powershell
streamlit run app.py
```

### Start just the crypto chatbot page

```powershell
streamlit run pages/chatbot.py
```

### Start the Ollama model

```powershell
ollama run llama3.1
```

Then open the Streamlit URL shown in the terminal.

## Deployment and Demo URL

Yes — you can share a demo by deploying the project and giving a public URL. If you host the Streamlit app on a service such as Streamlit Cloud, Render, Railway, or another web host, include that link in your GitHub README and project description.

- A local app usually runs at `http://localhost:8501`.
- A deployed demo URL should be public and reachable from other machines.
- If you use Streamlit Cloud, you can add the generated shareable URL directly to the README.

If you want to demonstrate the project without hosting, you can still describe the local run commands and include screenshots.

## How to Use

### Cipher Analysis Engine

1. Upload an encrypted file (`.bin`, `.dat`, or `.txt`).
2. Detect the algorithm.
3. Choose an intended data usage scenario.
4. Review the security strength and recommended algorithms.
5. Re-encrypt using a stronger supported algorithm if available.

### Crypto Chatbot

- Enter any cryptography question.
- The chatbot builds a system prompt and calls a local Ollama model.
- Use questions like:
  - `Compare AES and ChaCha20`
  - `Is MD5 secure?`
  - `Explain RSA encryption`

## Training Models (Optional)

If you want to recreate or update the detection models:

```powershell
python train.py
```

This script reads `features_enhanced.csv` and trains the stage-1 and stage-2 detection models used by the app.

## Troubleshooting

- If the chatbot shows a connection error, make sure Ollama is running and listening on `http://localhost:11434`.
- If the chatbot model fails, verify that `MODEL_NAME` in `crypto_chatbot/local_llm.py` matches an Ollama model returned by `ollama list`.
- If model files are missing, run `python train.py` to regenerate them (requires `features_enhanced.csv`).

## Notes

- The project is intended for academic learning and demonstration.
- The chatbot uses a local model and does not require cloud API keys.
- The analyzer uses machine learning ensembles to improve algorithm detection accuracy.

## Contact

For help, open an issue or contact the developer directly.
