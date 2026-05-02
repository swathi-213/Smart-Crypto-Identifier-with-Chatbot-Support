from crypto_chatbot.crypto_data import CRYPTO_ALGORITHMS

def build_system_prompt(intent: str, question: str) -> str:
    matched_algos = []

    for algo, info in CRYPTO_ALGORITHMS.items():
        if algo.lower() in question.lower():
            matched_algos.append(f"{algo}: {info}")

    grounding = (
        "\n".join(matched_algos)
        if matched_algos
        else "General cryptography principles."
    )

    return f"""
You are a cryptography expert chatbot.

User intent: {intent}

Rules:
- Answer only cryptography-related questions
- Do NOT recommend broken or deprecated algorithms
- Clearly warn if an algorithm is insecure
- Use simple explanations with technical correctness
- If comparison is asked, compare clearly
- If security is asked, mention attacks and risks

Known verified crypto facts:
{grounding}
"""