def detect_intent(question: str) -> str:
    q = question.lower()

    if "vs" in q or "compare" in q:
        return "comparison"
    if "attack" in q or "broken" in q or "secure" in q:
        return "security_analysis"
    if "how" in q or "explain" in q:
        return "explanation"

    return "general"