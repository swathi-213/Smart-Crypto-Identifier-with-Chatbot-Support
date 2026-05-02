CRYPTO_ALGORITHMS = {
    "AES": {
        "category": "Symmetric Block Cipher",
        "status": "Secure",
        "notes": "Used in TLS, disk encryption, VPNs"
    },
    "DES": {
        "category": "Symmetric Block Cipher",
        "status": "Broken",
        "notes": "56-bit key, brute-force attacks feasible"
    },
    "3DES": {
        "category": "Symmetric Block Cipher",
        "status": "Deprecated",
        "notes": "Vulnerable to meet-in-the-middle attacks"
    },
    "RSA": {
        "category": "Asymmetric Encryption",
        "status": "Secure if key ≥ 2048 bits",
        "notes": "Used for key exchange and signatures"
    },
    "ECC": {
        "category": "Asymmetric Encryption",
        "status": "Secure",
        "notes": "Smaller keys, better performance than RSA"
    },
    "MD5": {
        "category": "Hash Function",
        "status": "Broken",
        "notes": "Collision attacks exist"
    },
    "SHA-1": {
        "category": "Hash Function",
        "status": "Broken",
        "notes": "Chosen-prefix collisions"
    },
    "SHA-256": {
        "category": "Hash Function",
        "status": "Secure",
        "notes": "Used in blockchain and security systems"
    },
    "RC4": {
        "category": "Stream Cipher",
        "status": "Broken",
        "notes": "Severe statistical biases"
    },
    "ChaCha20": {
        "category": "Stream Cipher",
        "status": "Secure",
        "notes": "Modern alternative to RC4"
    }
}