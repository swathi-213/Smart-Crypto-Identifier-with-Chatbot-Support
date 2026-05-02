# =====================================================
# MODULE 4 : USAGE-RELATIVE SECURITY ANALYSIS (FINAL)
# =====================================================

# -----------------------------------------------------
# Helper: Normalize algorithm name to family
# -----------------------------------------------------
def normalize_algo(algo: str) -> str:
    """
    Converts algorithm name to its family.
    Examples:
    AES-CBC -> AES
    RSA-OAEP-2048 -> RSA
    SHA3-256 -> SHA3
    """
    if algo.startswith("SHA3"):
        return "SHA3"
    return algo.split("-")[0]


# -----------------------------------------------------
# Globally broken / deprecated algorithms
# -----------------------------------------------------
BROKEN_ALGORITHMS = {
    "MD5",
    "SHA1",
    "RIPEMD160",
    "RC4"
}


# -----------------------------------------------------
# SECURITY POLICY (COVERS ALL TRAINED ALGORITHMS)
# -----------------------------------------------------
SECURITY_POLICY = {

    "Secure Data Storage (Data at Rest)": {
        "strong": ["AES", "ChaCha20"],
        "medium": ["Blowfish", "CAST"],
        "weak": ["DES", "3DES"],
        "recommended_algorithms": ["AES-GCM", "AES-XTS"],
        "reencryption_supported": True,
        "reason": "Data at rest requires strong symmetric encryption resistant to offline attacks."
    },

    "Secure Data Communication (Data in Transit)": {
        "strong": ["AES", "ChaCha20"],
        "medium": [],
        "weak": ["DES", "3DES"],
        "recommended_algorithms": ["AES-GCM", "ChaCha20-Poly1305"],
        "reencryption_supported": True,
        "reason": "Data in transit requires authenticated encryption."
    },

    "Authentication & Integrity Verification": {
        "strong": ["SHA3", "HMAC", "RSA", "ECDSA"],
        "medium": [],
        "weak": ["MD5", "SHA1"],
        "recommended_algorithms": [
            "HMAC-SHA256",
            "SHA3-256",
            "RSA-PSS",
            "ECDSA"
        ],
        "reencryption_supported": False,
        "reason": "Integrity-focused use cases rely on hash functions and digital signatures."
    },

    "Key Exchange & Key Management": {
        "strong": ["RSA", "ECDH"],
        "medium": [],
        "weak": [],
        "recommended_algorithms": ["ECDH", "RSA-OAEP"],
        "reencryption_supported": False,
        "reason": "Key exchange relies on asymmetric cryptography."
    },

    "Real-Time Streaming Security": {
        "strong": ["ChaCha20"],
        "medium": ["AES"],
        "weak": ["DES", "3DES"],
        "recommended_algorithms": ["ChaCha20-Poly1305"],
        "reencryption_supported": True,
        "reason": "Low-latency encryption is required for real-time streaming."
    },

    "Financial Transactions": {
        "strong": ["AES", "RSA", "ECDSA"],
        "medium": [],
        "weak": ["DES"],
        "recommended_algorithms": ["AES-GCM", "ECDSA"],
        "reencryption_supported": True,
        "reason": "Financial systems require confidentiality, integrity, and non-repudiation."
    },

    "Healthcare / Sensitive Records": {
        "strong": ["AES"],
        "medium": [],
        "weak": ["DES"],
        "recommended_algorithms": ["AES-GCM"],
        "reencryption_supported": True,
        "reason": "Sensitive records require strong confidentiality."
    },

    "IoT / Embedded Device Security": {
        "strong": ["AES", "ChaCha20"],
        "medium": [],
        "weak": ["RSA"],
        "recommended_algorithms": ["AES-CCM"],
        "reencryption_supported": True,
        "reason": "IoT devices require lightweight and efficient cryptography."
    },

    "Cloud & Distributed Systems": {
        "strong": ["AES", "ChaCha20"],
        "medium": [],
        "weak": ["AES-CBC"],
        "recommended_algorithms": ["AES-GCM"],
        "reencryption_supported": True,
        "reason": "Cloud systems require scalable authenticated encryption."
    },

    "Archival / Long-Term Protection": {
        "strong": ["AES"],
        "medium": [],
        "weak": ["DES", "SHA1"],
        "recommended_algorithms": ["AES-XTS"],
        "reencryption_supported": True,
        "reason": "Archived data must remain secure over long periods."
    }
}


# -----------------------------------------------------
# Strength classifier (NO Unknown / Not Applicable)
# -----------------------------------------------------
def classify_strength(family: str, policy: dict) -> str:
    if family in policy.get("strong", []):
        return "Strong"
    if family in policy.get("medium", []):
        return "Medium"
    return "Weak"


# -----------------------------------------------------
# MAIN ANALYSIS FUNCTION
# -----------------------------------------------------
def analyze_security_by_usage(detected_algorithm: str, data_usage: str):
    """
    Determines algorithm strength relative to data usage
    and whether re-encryption is required.
    """

    if data_usage not in SECURITY_POLICY:
        raise ValueError("Invalid data usage selection")

    policy = SECURITY_POLICY[data_usage]
    family = normalize_algo(detected_algorithm)

    # -------- Explicit broken algorithm handling --------
    if family in BROKEN_ALGORITHMS:
        return {
            "detected_algorithm": detected_algorithm,
            "algorithm_family": family,
            "data_usage": data_usage,
            "strength_for_usage": "Weak",
            "recommended_algorithms": policy["recommended_algorithms"],
            "reencryption_supported": policy["reencryption_supported"],
            "reason": (
                f"{family} is cryptographically broken due to known attacks "
                "such as collision or statistical bias attacks."
            )
        }

    # -------- Integrity / Authentication override --------
    strength = classify_strength(family, policy)

    return {
        "detected_algorithm": detected_algorithm,
        "algorithm_family": family,
        "data_usage": data_usage,
        "strength_for_usage": strength,
        "recommended_algorithms": policy["recommended_algorithms"],
        "reencryption_supported": policy["reencryption_supported"],
        "reason": policy["reason"]
    }